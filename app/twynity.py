"""Twynity-specific HTTP routes for Higgfield MCP.

Provides authenticated project-scoped endpoints for the Twynity platform.
"""

from typing import Any

from fastapi import APIRouter, HTTPException

from app.auth import get_identity
from app.config import settings

router = APIRouter()


@router.get("/api/v1/.well-known/mcp.json")
async def get_public_manifest() -> dict[str, Any]:
    """Public manifest with external_connections for Twynity.

    This endpoint mirrors the manifest route but returns a format
    compatible with Twynity's external connections framework.

    Args:
        Returns service metadata.

    Raises:
        HTTPException: If request is not authenticated
    """
    identity = await get_identity(router)

    return {
        "version": settings.APP_VERSION,
        "name": settings.APP_TITLE,
        "description": "Higgfield MCP - API key management and generation server",
        "identity": {
            "user_id": identity.user_id,
            "persona_id": identity.persona_id,
        },
        "external_connections": {
            "project": {
                "type": "http",
                "api_path": settings.API_V1_STR,
                "description": f"Project-scoped API for {settings.APP_TITLE}",
            }
        },
    }


@router.get("/api/v1/schema")
async def get_configuration_schema() -> dict[str, Any]:
    """Public configuration schema endpoint.

    Returns configuration schema information without secrets.

    Args:
        Returns schema information.

    Raises:
        HTTPException: If request is not authenticated
    """
    identity = await get_identity(router)

    return {
        "service_id": settings.SERVICE_ID,
        "user_id": identity.user_id,
        "persona_id": identity.persona_id,
        "title": settings.APP_TITLE,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "api_version": "v1",
    }


@router.get("/api/v1/configuration")
async def get_configuration() -> dict[str, Any]:
    """Get safe configuration metadata.

    Returns only metadata without credentials or secrets.

    Args:
        Returns configuration metadata.

    Raises:
        HTTPException: If request is not authenticated
    """
    identity = await get_identity(router)

    return {
        "service_id": settings.SERVICE_ID,
        "user_id": identity.user_id,
        "persona_id": identity.persona_id,
        "title": settings.APP_TITLE,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "features": {
            "api_key_management": True,
            "generation_tracking": True,
            "external_api_calls": True,
        },
    }


@router.get("/api/v1/external-connection/me")
async def get_current_connection() -> dict[str, Any]:
    """Get current user's external connection status.

    Returns connection status and metadata.

    Args:
        Returns connection status.

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
        "api_key_count": 0,  # Would be populated by actual storage
    }


@router.post("/api/v1/configuration")
async def update_configuration(body: dict[str, Any]):
    """Update user configuration.

    Args:
        body: Configuration data to update

    Returns:
        Updated configuration

    Raises:
        HTTPException: If request is not authenticated or update fails
    """
    identity = await get_identity(router)

    # In production, this would update the user's configuration in storage
    # For now, return acknowledgment
    return {
        "status": "success",
        "user_id": identity.user_id,
        "persona_id": identity.persona_id,
        "updated": list(body.keys()),
    }