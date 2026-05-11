import logging
from functools import lru_cache

from twilio.rest import Client

from .config import WHATSAPP_MAX_CHARS, load_settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _client() -> Client:
    settings = load_settings()
    return Client(settings.twilio_account_sid, settings.twilio_auth_token)


def _chunk(text: str, size: int = WHATSAPP_MAX_CHARS) -> list[str]:
    """Divide texto largo en pedazos <= size, cortando en saltos de linea
    cuando es posible para no partir oraciones a la mitad."""
    if len(text) <= size:
        return [text]

    chunks: list[str] = []
    remaining = text
    while len(remaining) > size:
        cut = remaining.rfind("\n", 0, size)
        if cut == -1 or cut < size // 2:
            cut = remaining.rfind(" ", 0, size)
        if cut == -1 or cut < size // 2:
            cut = size
        chunks.append(remaining[:cut].rstrip())
        remaining = remaining[cut:].lstrip()
    if remaining:
        chunks.append(remaining)
    return chunks


def send_whatsapp(to_phone: str, body: str) -> list[str]:
    """Envia un mensaje (o varios si excede 1600 chars) via Twilio.
    Devuelve los SIDs de los mensajes enviados."""
    settings = load_settings()
    client = _client()

    to = to_phone if to_phone.startswith("whatsapp:") else f"whatsapp:{to_phone}"
    pieces = _chunk(body)
    sids: list[str] = []
    for piece in pieces:
        msg = client.messages.create(
            from_=settings.twilio_whatsapp_number,
            to=to,
            body=piece,
        )
        sids.append(msg.sid)
        logger.info("WhatsApp enviado to=%s sid=%s len=%d", to, msg.sid, len(piece))
    return sids


def truncate_for_twiml(body: str) -> str:
    """Para respuestas via TwiML inline (caso /webhook), Twilio acepta
    un solo mensaje. Truncamos al limite con elipsis."""
    if len(body) <= WHATSAPP_MAX_CHARS:
        return body
    return body[: WHATSAPP_MAX_CHARS - 3] + "..."
