"""Authentication contract tests."""

import pytest
from fastapi import HTTPException

from app.auth import get_identity, get_identity_from_headers, TwynityIdentity
from app.core.authentication.auth_middleware import get_current_token


class TestJWTVerification:
    """Tests for JWT authentication verification."""

    def test_invalid_token_missing_header(self):
        """Test that missing Authorization header raises error."""
        from starlette.requests import Request

        request = Request({"type": "http", "headers": []})

        with pytest.raises(HTTPException) as exc_info:
            get_current_token(request)
        assert exc_info.value.status_code == 401

    def test_invalid_token_wrong_scheme(self):
        """Test that non-bearer tokens are rejected."""
        from starlette.requests import Request

        request = Request(
            {
                "type": "http",
                "headers": [("authorization", "Basic invalid-token")],
            }
        )

        with pytest.raises(HTTPException) as exc_info:
            get_current_token(request)
        assert exc_info.value.status_code == 401

    def test_invalid_token_missing_persona_id(self):
        """Test that missing Persona-Id header raises error."""
        import httpx
        from unittest.mock import AsyncMock, patch
        from starlette.requests import Request

        mock_response = AsyncMock()
        mock_response.raise_for_status = lambda: None
        mock_response.json.return_value = {"keys": []}

        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.return_value.__aenter__.return_value = mock_response

            request = Request(
                {
                    "type": "http",
                    "headers": [("authorization", "Bearer fake-token")],
                }
            )

            with pytest.raises(HTTPException) as exc_info:
                get_identity_from_headers(request.headers)
            assert exc_info.value.status_code == 400
            assert "Persona-Id" in exc_info.value.detail

    def test_valid_token_with_persona_id(self):
        """Test that valid token with Persona-Id succeeds."""
        import httpx
        from unittest.mock import AsyncMock, patch
        from starlette.requests import Request

        jwks_response = {
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

        mock_response = AsyncMock()
        mock_response.raise_for_status = lambda: None
        mock_response.json.return_value = jwks_response

        with patch("httpx.AsyncClient.get") as mock_get, patch("httpx.AsyncClient.request") as mock_request:
            mock_get.return_value.__aenter__.return_value = mock_response
            mock_request.return_value.json.return_value = {"test": "data"}

            headers = {
                "authorization": "Bearer fake-token",
                "persona-id": "test-persona",
            }

            result = get_identity_from_headers(headers)
            assert isinstance(result, TwynityIdentity)
            assert result.user_id == "test-user"  # From mock token
            assert result.persona_id == "test-persona"


class TestIdentityDataclass:
    """Tests for identity dataclass."""

    def test_twynity_identity_is_frozen(self):
        """Test that TwynityIdentity is an immutable dataclass."""
        identity = TwynityIdentity(user_id="test", persona_id="test")
        assert identity.user_id == "test"
        assert identity.persona_id == "test"

        # Should raise TypeError if trying to modify
        try:
            identity.user_id = "modified"
            assert False, "Should have raised TypeError"
        except TypeError:
            pass

    def test_twynity_identity_comparison(self):
        """Test identity equality."""
        identity1 = TwynityIdentity(user_id="test", persona_id="test")
        identity2 = TwynityIdentity(user_id="test", persona_id="test")
        identity3 = TwynityIdentity(user_id="test", persona_id="other")

        assert identity1 == identity2
        assert identity1 != identity3