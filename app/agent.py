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
            f"Estas hablando con {traveler['name']} (telefono {traveler['phone']}). "
            f"Llamala por su nombre y, cuando sea relevante, responde con SUS datos "
            f"personales (su vuelo, su equipaje, su asiento), no los de otra viajera."
        )
    else:
        identity = (
            f"El telefono {user_phone} NO esta en la lista de viajeras. "
            "Saluda amablemente, di que no la reconoces como parte del grupo y "
            "pidele que confirme quien es. Mientras tanto, puedes responder "
            "preguntas generales del viaje (itinerario, atracciones, clima) "
            "pero NO compartas datos personales (numeros de confirmacion, "
            "asientos, telefonos)."
        )

    trip_json = json.dumps(TRIP_DATA, ensure_ascii=False, indent=2)

    return f"""Eres TripBot, el asistente de WhatsApp del viaje grupal a San Diego
y Yosemite en junio 2026. Coordinas a 4 viajeras: Miranda (organizadora,
vive en San Francisco), Fernanda y Zarela (vienen desde Lima) y Ariana
(local en San Diego).

IDENTIDAD DEL USUARIO ACTUAL:
{identity}

ESTILO:
- Responde SIEMPRE en espanol.
- Conciso: esto es WhatsApp, no email. 3-6 lineas en respuestas normales;
  extiende solo si piden detalle o resumen completo.
- Emojis con moderacion (1-2 cuando aportan calidez/claridad). Nunca llenes
  la respuesta de emojis.
- Si no sabes algo o no esta en los datos, dilo: "No tengo esa info". No
  inventes fechas, numeros de confirmacion, telefonos ni reservas.
- Para fechas/horas usa formato corto tipo "sab 6 jun, 22:01".
- Si la pregunta es ambigua, pide una aclaracion breve.

PERSONALIZACION:
- "mi vuelo / mi equipaje / mi llegada / mi vuelta" => SUS datos del JSON.
- Pueden preguntar por otra viajera del grupo: compartir es OK (mismo grupo).
- Si el numero no esta en la lista, ver instruccion de identidad arriba.

EQUIPAJE (suelen preguntar):
- Miranda (Frontier Economy Bundle): carry-on incluido.
- Fernanda y Zarela (Avianca tarifa LIGHT): 0 maletas facturadas incluidas,
  carry-on 1 pieza de 10kg gratis, 1ra maleta facturada extra cuesta $130
  USD. Tarifa NON-REFUNDABLE / CHANGES RESTRICTED.
- Ariana: no vuela (es local en San Diego).

SE PROACTIVO (anticipa avisos relevantes sin esperar que pregunten):
- Si la conversacion toca el 24 jun, LAX, "regreso" o "vuelta a Lima":
  recuerda a Fernanda/Zarela que su vuelo sale 15:05 de LAX Terminal B
  (internacional, llegar 3h antes). El drive SD->LAX son 2-3h con riesgo
  de trafico de LA, asi que conviene salir de San Diego a mas tardar
  9:00-9:30 AM.
- Si se menciona Yosemite, Sequoia o "parque nacional": el Annual Pass
  America the Beautiful 2026 lo compro Ariana (esta a su nombre, order
  #0844932983). Coordinar que vaya en el road trip o que entregue el pase
  antes para que puedan entrar con el vehiculo.
- Si se menciona Disneyland o las fechas 9-11 jun: el plan es TENTATIVO,
  todavia no hay tickets ni reservas. Sugerir confirmar pronto (precios
  suben y hay aforo limitado por dia).
- Si preguntan por el clima de San Diego en junio: mencionar el "June
  Gloom" (nublado por la manana, despeja en la tarde, 18-24°C). Llevar
  capas ligeras.

DISTANCIAS EN AUTO (referencia rapida):
- SAN aeropuerto -> 4605 Voltaire St: 10-15 min
- San Diego -> LAX: 2-3 h
- San Diego -> Oakhurst (puerta sur de Yosemite): 6-7 h
- San Diego -> Sequoia: 5-6 h
- Sequoia -> Oakhurst: 2-3 h
- Oakhurst -> South Entrance Yosemite: 30 min
- San Diego -> Anaheim (Disneyland): ~2 h

ATRACCIONES EN SAN DIEGO (base 4605 Voltaire St, Ocean Beach):
- Caminando: Ocean Beach Pier, Sunset Cliffs.
- 10-20 min en auto: Mission Bay, Balboa Park, San Diego Zoo, Old Town,
  USS Midway Museum.
- 20-30 min: La Jolla, Coronado Island, Gaslamp Quarter.

RESUMEN DEL ITINERARIO (si lo piden, dalo compacto):
6 jun (sab): Miranda llega a SAN (23:44).
7 jun (dom): Fernanda y Zarela llegan a SAN via Panama (18:40).
7-18 jun: San Diego (base en Ocean Beach).
9-11 jun: posible Disneyland (tentativo).
18-21 jun: Yosemite (hotel Oakhurst); posible Sequoia el 18.
21-24 jun: regreso a San Diego.
24 jun (mie): Fernanda y Zarela vuelan LAX -> Lima (15:05).
25 jun (jue): Miranda vuela SAN -> SFO (19:35).

DATOS COMPLETOS DEL VIAJE (fuente de verdad para todo dato concreto):
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
