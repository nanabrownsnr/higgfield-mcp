"""Service configuration and logging setup."""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

from pydantic_settings import BaseSettings

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Service identity
    SERVICE_ID: str = os.getenv("SERVICE_ID", "higgfield-mcp")
    APP_TITLE: str = "Higgfield MCP"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    ENVIRONMENT_NAME: str = os.getenv("ENVIRONMENT_NAME", "development")
    API_V1_STR: str = "/api/v1"
    ROOT_PATH: str = ""

    # Security
    ALLOWED_ORIGINS: str = "*"
    PERSONA_ID_HEADER: str = "Persona-Id"

    # Account Service (JWT verification)
    ACCOUNT_SERVICE_URL: str = os.getenv("ACCOUNT_SERVICE_URL", "http://account_service:8000")
    ACCOUNT_SERVICE_JWKS_ENDPOINT: str = os.getenv("ACCOUNT_SERVICE_JWKS_ENDPOINT", "/.well-known/jwks.json")
    ACCOUNT_SERVICE_JWKS_CACHE_TTL: int = int(os.getenv("ACCOUNT_SERVICE_JWKS_CACHE_TTL", "300"))
    ALLOWED_TOKEN_CLIENTS: str = "*"

    # Usage Reporting
    USAGE_REPORT_ENDPOINT: str = os.getenv("USAGE_REPORT_ENDPOINT", "/api/v1/usage")

    # MongoDB
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://mongo:27017")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "higgfield")
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "REPLACE_WITH_32_CHAR_KEY_FOR_FERNET")

    # License Server (optional)
    LICENSE_KEY: str = os.getenv("LICENSE_KEY", "REPLACE_WITH_KEY")
    LICENSE_SERVER_BASE_URL: str = os.getenv("LICENSE_SERVER_BASE_URL", "https://license-server.example.com")
    LICENSE_SERVER_JWKS_ENDPOINT: str = os.getenv("LICENSE_SERVER_JWKS_ENDPOINT", "/.well-known/jwks.json")
    LICENSE_SERVER_ACTIVATION_ENDPOINT: str = os.getenv("LICENSE_SERVER_ACTIVATION_ENDPOINT", "/api/v1/activate")

    # File Storage (optional)
    FILE_STORAGE_URL: str = os.getenv("FILE_STORAGE_URL", "https://file-storage.example.com")
    QUEST_CLIENT_ID: str = os.getenv("QUEST_CLIENT_ID", "")
    QUEST_CLIENT_SECRET: str = os.getenv("QUEST_CLIENT_SECRET", "")

    # OpenAI (if using GPT integration)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")


# Configure logging
def setup_logging() -> None:
    """Configure application logging."""
    log_level = "DEBUG" if Settings().ENVIRONMENT_NAME == "development" else "INFO"
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            TimedRotatingFileHandler(
                "logs/higgfield.log",
                when="midnight",
                backupCount=30,
                encoding="utf-8",
            ),
        ],
    )


settings = Settings()
setup_logging()