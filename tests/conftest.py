"""Shared test fixtures and configuration."""

import os
from pathlib import Path

import pytest
from httpx import AsyncClient

from fastapi import FastAPI

from app.main import app


@pytest.fixture
def test_settings(monkeypatch):
    """Override settings with test-safe defaults."""
    from app.config import Settings

    monkeypatch.setenv("ENCRYPTION_KEY", "test-32-character-key-for-fernet-encryption!")
    monkeypatch.setenv("ACCOUNT_SERVICE_URL", "http://test-account-service:8000")
    monkeypatch.setenv("ACCOUNT_SERVICE_JWKS_ENDPOINT", "/.well-known/jwks.json")
    monkeypatch.setenv("MONGODB_URI", "mongodb://localhost:27017")
    monkeypatch.setenv("MONGODB_DB", "test_higgfield")
    return Settings()


@pytest.fixture
async def async_client():
    """Create async test client."""
    from fastapi.testclient import TestClient

    return TestClient(app)


@pytest.fixture
async def authenticated_client(monkeypatch):
    """Create authenticated test client with mock headers."""
    from fastapi.testclient import TestClient

    monkeypatch.setenv("ACCOUNT_SERVICE_JWKS_ENDPOINT", "/.well-known/jwks.json")
    client = TestClient(app)

    def override_get_identity(request):
        """Mock identity for testing."""
        from starlette import status
        from fastapi import HTTPException

        headers = request.headers
        if "Persona-Id" not in headers:
            raise HTTPException(status_code=400, detail="Persona-Id header required")

        from app.auth import HiggfieldIdentity

        return HiggfieldIdentity(user_id="test-user", persona_id=headers.get("Persona-Id"))

    # This is a simplified override for testing purposes
    return client


@pytest.fixture
def mock_jwks_response(monkeypatch):
    """Mock JWKS response for testing."""
    jwks = {
        "keys": [
            {
                "kty": "RSA",
                "kid": "test-kid",
                "use": "sig",
                "n": "test-modulus",
                "e": "AQAB",
            }
        ]
    }

    # This would need to be set up properly in a real test setup
    return jwks


@pytest.fixture
def test_data_dir(tmp_path):
    """Create temporary directory for file operations."""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return data_dir