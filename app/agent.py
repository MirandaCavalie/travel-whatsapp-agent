import json
import logging
from collections import defaultdict, deque
from functools import lru_cache
from threading import Lock

from anthropic import Anthropic

from .config import CLAUDE_MODEL, MAX_HISTORY_MESSAGES, load_settings
from .trip_data import TRIP_DATA, find_traveler_by_phone

logger = logging.getLogger(__name__)


# Historial por telefono. Cada entrada es {"role": "user"|"assistant", "content": str}.
# deque con maxlen garantiza que no crezca sin limite.
_history: dict[str, deque] = defaultdict(lambda: deque(maxlen=MAX_HISTORY_MESSAGES))
_history_lock = Lock()


@lru_cache(maxsize=1)
def _client() -> Anthropic:
    settings = load_settings()
    return Anthropic(api_key=settings.anthropic_api_key)


def _build_system_prompt(user_phone: str) -> str:
    traveler = find_traveler_by_phone(user_phone)
    if traveler:
        identity = (
            f"Estas hablando con {traveler['name']} "
            f"(telefono {traveler['phone']}). "
            "Trata sus consultas con contexto personal cuando aplique."
        )
    else:
        identity = (
            f"El telefono {user_phone} NO esta en la lista de viajeros. "
            "Responde igual pero menciona que no lo reconoces como parte del grupo "
            "y pide que confirme quien es."
        )

    trip_json = json.dumps(TRIP_DATA, ensure_ascii=False, indent=2)

    return f"""Eres el asistente de WhatsApp de un viaje grupal. Tu trabajo es
ayudar a coordinar al grupo respondiendo preguntas sobre el viaje.

IDENTIDAD DEL USUARIO:
{identity}

REGLAS:
- Responde siempre en espanol.
- Se conciso: WhatsApp, no email. Maximo 5-6 lineas salvo que pidan detalle.
- Tono amigable pero directo. Sin emojis salvo que el usuario los use primero.
- Si te preguntan algo que NO esta en los datos del viaje (abajo), di
  claramente "No tengo esa info" en vez de inventar.
- Si te preguntan por OTRO viajero, puedes compartir datos relevantes
  (vuelos, telefono de contacto) porque son del mismo grupo.
- Para fechas/horas, usa formato claro tipo "lunes 10 jul, 15:00".
- Si la pregunta es ambigua, pide una aclaracion corta.

DATOS DEL VIAJE (JSON):
{trip_json}
"""


def _append_history(phone: str, role: str, content: str) -> None:
    with _history_lock:
        _history[phone].append({"role": role, "content": content})


def _get_history_messages(phone: str) -> list[dict]:
    with _history_lock:
        return list(_history[phone])


def get_response(user_message: str, user_phone: str) -> str:
    """Llama a Claude con el mensaje del usuario + historial y devuelve la respuesta."""
    _append_history(user_phone, "user", user_message)

    try:
        response = _client().messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            system=_build_system_prompt(user_phone),
            messages=_get_history_messages(user_phone),
        )
        # La respuesta puede tener varios bloques; tomamos el texto.
        parts = [block.text for block in response.content if getattr(block, "type", None) == "text"]
        reply = "\n".join(parts).strip() or "(respuesta vacia)"
    except Exception:
        logger.exception("Error llamando a Claude API para %s", user_phone)
        # No guardamos la respuesta de error en historial: que el siguiente
        # turno empiece limpio sin un assistant message fallido.
        return "Hubo un error, intenta de nuevo."

    _append_history(user_phone, "assistant", reply)
    logger.info("Claude respondio phone=%s in_len=%d out_len=%d",
                user_phone, len(user_message), len(reply))
    return reply


def reset_history(phone: str) -> None:
    """Util para tests o comandos admin."""
    with _history_lock:
        _history.pop(phone, None)
