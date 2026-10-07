"""MCP manifest endpoints.

Provides well-known manifest endpoints for MCP service discovery and configuration.
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.auth import get_identity
from app.config import settings

router = APIRouter()


class ManifestResponse(BaseModel):
    """MCP manifest response model."""

    version: str
    name: str
    description: str
    capabilities: dict[str, Any]
    external_connections: dict[str, Any]


@router.get("/.well-known/mcp.json", response_model=ManifestResponse)
async def get_manifest() -> ManifestResponse:
    """Public manifest endpoint for MCP service discovery.

    Returns service metadata without authentication required.
    """
    return ManifestResponse(
        version=settings.APP_VERSION,
        name=settings.APP_TITLE,
        description="Higgfield MCP - API key management and generation server",
        capabilities={
            "tools": ["list_api_keys", "create_api_key", "list_generations", "call_external"],
            "resources": ["api_key_storage", "generation_history"],
        },
        external_connections={
            "project": {
                "type": "http",
                "api_path": "/api/v1",
                "description": "Higgfield MCP project API",
            }
        },
    )


@router.get("/schema", response_model=dict[str, Any])
async def get_schema() -> dict[str, Any]:
    """Public configuration schema endpoint.

    Returns schema information without authentication.
    """
    return {
        "service_id": settings.SERVICE_ID,
        "title": settings.APP_TITLE,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "api_version": "v1",
        "features": {
            "api_key_management": True,
            "generation_tracking": True,
            "external_api_calls": True,
            "file_operations": True,
        },
    }


@router.get("/health")
async def health_check():
    """Health check endpoint.

    Returns service health status without authentication.
    """
    return {"status": "healthy", "service": settings.APP_TITLE}