# app/config.py
import logging, os
from logging.handlers import TimedRotatingFileHandler
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Basic identity
    SERVICE_ID: str = os.getenv("SERVICE_ID", "api_key_mcp")
    APP_TITLE: str = "API-Key MCP"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    ROOT_PATH: str = ""

    # Auth / JWKS
    ALLOWED_ORIGINS: str = "*"
    ACCOUNT_SERVICE_URL: str = "http://account_service:8000"
    ACCOUNT_SERVICE_JWKS_ENDPOINT: str = "/.well-known/jwks.json"
    ACCOUNT_SERVICE_JWKS_CACHE_TTL: int = 300
    ALLOWED_TOKEN_CLIENTS: str = "*"
    USAGE_REPORT_ENDPOINT: str = "/api/v1/usage"

    # MongoDB
    MONGODB_URI: str = "mongodb://mongo:27017"
    PERSONA_ID_HEADER: str = "Persona-Id"
    ENCRYPTION_KEY: str = "REPLACE_WITH_REAL_FERNET_KEY"

    # License server
    LICENSE_KEY: str = "REPLACE_WITH_ACTIVATION_KEY"
    LICENSE_SERVER_BASE_URL: str = "https://license.4th-ir.io"
    LICENSE_SERVER_JWKS_ENDPOINT: str = "/.well-known/jwks.json"
    LICENSE_SERVER_ACTIVATION_ENDPOINT: str = "/api/v1/activate"

    # File service (optional)
    FILE_STORAGE_URL: str = "https://file.4th-ir.io"
    QUEST_CLIENT_ID: str = ""
    QUEST_CLIENT_SECRET: str = ""

settings = Settings()
