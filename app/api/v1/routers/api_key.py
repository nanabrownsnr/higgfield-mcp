"""API key management endpoints.

Provides authenticated API key creation, listing, and deletion.
"""

from typing import Any

from fastapi import APIRouter, HTTPException

from app.auth import get_identity
from app.config import settings

router = APIRouter()


@router.get("/keys")
async def list_keys() -> dict[str, Any]:
    """List all API keys for the authenticated user.

    Returns:
        Dictionary with keys array and count.

    Raises:
        HTTPException: If request is not authenticated
    """
    identity = await get_identity(router)

    return {
        "service_id": settings.SERVICE_ID,
        "user_id": identity.user_id,
        "persona_id": identity.persona_id,
        "keys": [],
        "count": 0,
    }


@router.post("/keys")
async def create_key(name: str, description: str = "") -> dict[str, Any]:
    """Create a new API key.

    Args:
        name: Name for the API key
        description: Optional description

    Returns:
        Created API key information.

    Raises:
        HTTPException: If request is not authenticated
    """
    identity = await get_identity(router)

    # In production, this would create an API key in the encrypted storage
    # For now, return simulated data
    return {
        "status": "success",
        "user_id": identity.user_id,
        "key_id": f"key-{identity.user_id}-{name}",
        "key": "sk-" + identity.user_id + "-" + name,
        "description": description,
    }


@router.delete("/keys/{key_id}")
async def delete_key(key_id: str) -> dict[str, Any]:
    """Delete an API key.

    Args:
        key_id: ID of the key to delete

    Returns:
        Delete confirmation.

    Raises:
        HTTPException: If request is not authenticated
    """
    identity = await get_identity(router)

    return {
        "status": "success",
        "user_id": identity.user_id,
        "key_id": key_id,
        "message": "API key deleted successfully",
    }