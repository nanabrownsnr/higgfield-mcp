"""API v1 endpoints package."""

from app.api.v1.routers import keys, generations  # noqa: F401
from app.api.v1.manifest import router as manifest_router
from app.api.v1.health import router as health_router

__all__ = [
    "manifest_router",
    "health_router",
]