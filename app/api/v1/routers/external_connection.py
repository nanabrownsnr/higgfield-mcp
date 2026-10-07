"""External connection endpoints for API v1 routers.

Provides authentication-scoped connection management APIs.
"""

from typing import Any

from fastapi import APIRouter, HTTPException

from app.auth import get_identity
from app.config import settings

router = APIRouter()


@router.get("/external-connection/me")
async def get_current_connection() -> dict[str, Any]:
    """Get current user's external connection status.

    Returns connection status for the authenticated user.

    Args:
        Returns:
            Connection status including API key information

    Raises:
        HTTPException: If request is not authenticated
    """
    identity = await get_identity(router)

    return {
        "service_id": settings.SERVICE_ID,
        "user_id": identity.user_id,
        "persona_id": identity.persona_id,
        "status": "connected",
        "has_credentials": True,
    }


# Keep backward compatibility
@router.get("/health")
async def health() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "healthy"}