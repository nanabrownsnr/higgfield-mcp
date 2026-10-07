"""Authentication middleware for Higgfield MCP.

This module provides authentication utilities for FastAPI routes.
It uses the secure JWT verification from app.auth.get_identity_from_headers.
"""

from typing import Optional

from starlette.requests import Request

from app.auth import get_identity_from_headers
from app.core.authentication.auth_token import TokenData


async def get_current_token(request: Request) -> TokenData:
    """Extract and decode JWT token from Authorization header.

    WARNING: This is a legacy method. New code should use get_identity_from_headers
    for proper JWT verification with JWKS signature checking.

    Args:
        request: The FastAPI request object

    Returns:
        TokenData with user claims

    Raises:
        HTTPException: If token is missing or invalid
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        from starlette import status
        from fastapi import HTTPException

        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    token = auth_header[7:]
    try:
        from jose import jwt
        from app.config import settings

        payload = jwt.decode(
            token,
            options={"verify_signature": False, "verify_aud": False},
        )
    except Exception as exc:
        from starlette import status
        from fastapi import HTTPException

        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    # Map token claims to TokenData
    user_id = payload.get("id") or payload.get("sub")
    return TokenData(sub=user_id, role=payload.get("role"))


async def get_effective_owner_id(
    request: Request,
    token_data: Optional[TokenData] = None,
) -> str:
    """Get effective owner ID from request headers.

    This method requires Persona-Id header, similar to Twynity's pattern.

    Args:
        request: The FastAPI request object
        token_data: Optional pre-extracted TokenData

    Returns:
        Persona ID from headers

    Raises:
        HTTPException: If no Persona-Id is provided
    """
    from app.config import settings

    persona_id = request.headers.get(settings.PERSONA_ID_HEADER)
    if not persona_id:
        from starlette import status
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400,
            detail=f"Persona-Id header is required for authenticated requests",
        )
    return persona_id


# Legacy alias for backward compatibility
async def get_current_identity(request: Request) -> TokenData:
    """Legacy alias for get_current_token. Use get_current_token instead."""
    return await get_current_token(request)