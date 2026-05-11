import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


@dataclass(frozen=True)
class Settings:
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_whatsapp_number: str
    anthropic_api_key: str
    environment: str
    public_base_url: str

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(
            f"Falta la variable de entorno {name}. "
            f"Revisa tu .env (copia .env.example si aun no lo hiciste)."
        )
    return value


def load_settings() -> Settings:
    return Settings(
        twilio_account_sid=_required("TWILIO_ACCOUNT_SID"),
        twilio_auth_token=_required("TWILIO_AUTH_TOKEN"),
        twilio_whatsapp_number=_required("TWILIO_WHATSAPP_NUMBER"),
        anthropic_api_key=_required("ANTHROPIC_API_KEY"),
        environment=os.getenv("ENVIRONMENT", "development").strip(),
        public_base_url=os.getenv("PUBLIC_BASE_URL", "").strip(),
    )


CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_HISTORY_MESSAGES = 20
WHATSAPP_MAX_CHARS = 1600
