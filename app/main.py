import logging

from fastapi import FastAPI, Form, HTTPException, Request, Response
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from .agent import get_response
from .config import load_settings
from .whatsapp import truncate_for_twiml

logger = logging.getLogger(__name__)

app = FastAPI(title="Travel WhatsApp Agent")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


async def _validate_twilio_signature(request: Request, form: dict) -> None:
    """En produccion, exigimos firma valida de Twilio. En dev, solo log."""
    settings = load_settings()
    signature = request.headers.get("X-Twilio-Signature", "")

    # URL publica: si PUBLIC_BASE_URL esta seteada la usamos (ngrok/dominio),
    # si no usamos la URL que ve FastAPI (puede no coincidir detras de proxy).
    if settings.public_base_url:
        url = settings.public_base_url.rstrip("/") + request.url.path
    else:
        url = str(request.url)

    validator = RequestValidator(settings.twilio_auth_token)
    valid = validator.validate(url, form, signature)

    if not valid:
        if settings.is_production:
            logger.warning("Twilio signature invalida url=%s", url)
            raise HTTPException(status_code=403, detail="Invalid Twilio signature")
        else:
            logger.warning("Twilio signature invalida (dev, permitiendo) url=%s", url)


@app.post("/webhook/whatsapp")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...),
) -> Response:
    form = dict(await request.form())
    await _validate_twilio_signature(request, form)

    logger.info("WhatsApp recibido from=%s body=%r", From, Body)

    try:
        reply = get_response(user_message=Body, user_phone=From.replace("whatsapp:", ""))
    except Exception:
        logger.exception("Error procesando mensaje de %s", From)
        reply = "Hubo un error, intenta de nuevo."

    twiml = MessagingResponse()
    twiml.message(truncate_for_twiml(reply))
    return Response(content=str(twiml), media_type="application/xml")
