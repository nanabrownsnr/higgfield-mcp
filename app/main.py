"""Application entry point and server setup for Higgfield MCP."""

import asyncio
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware

from fastmcp import FastMCP
from mcp.server import Server

import httpx

from app.config import settings, setup_logging
from app.core.license_server import license_watcher
from app.tools.generational import register_tools as register_gen_tools
from app.tools.files import register_tools as register_files_tools
from app.tools.render_content import register_tools as register_render_tools
from app.api.v1.manifest import router as manifest_router
from app.api.v1.health import router as health_router
from app.api.v1.routers.api_key import router as keys_router
from app.api.v1.routers.generations import router as generations_router
from app.twynity import router as twynity_router

# Import auth for FastMCP's JWT verifier
from app.auth import get_auth_provider


# ---------- Usage tracking ----------
async def track_usage(request: Request) -> None:
    """Capture usage metrics and send to reporting endpoint."""
    if "Authorization" not in request.headers:
        return

    try:
        data = {
            "service": settings.APP_TITLE,
            "method": request.method,
            "endpoint": str(request.url),
            "timestamp": datetime.now(UTC).timestamp(),
            "ip_address": request.client.host,
        }

        async with httpx.AsyncClient() as client:
            await client.post(settings.USAGE_REPORT_ENDPOINT, json=data)
    except Exception:
        pass


# ---------- FastAPI app ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    setup_logging()
    asyncio.create_task(license_watcher())
    yield


app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    root_path=settings.ROOT_PATH,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Usage tracking middleware
@app.middleware("http")
async def usage_middleware(request: Request, call_next):
    """Middleware to track request usage."""
    # Don't track non-API routes or manifest endpoints
    if "/api/v1" not in str(request.url):
        return await call_next(request)

    # Start tracking asynchronously
    asyncio.create_task(track_usage(request))
    return await call_next(request)


@app.get("/", include_in_schema=False)
async def index_redirect() -> dict[str, str]:
    """Redirect root to API docs."""
    return {"message": "Higgfield MCP", "docs": f"{settings.ROOT_PATH}/docs"}


# ---------- MCP tool routers ----------
from app.tools.api_call import register_tools as register_api_tools

register_tools(Server(app))
register_api_tools(Server(app))
register_gen_tools(Server(app))
register_files_tools(Server(app))
register_render_tools(Server(app))


# ---------- MCP server setup ----------
mcpapp = FastMCP(
    app,
    auth=get_auth_provider(),
    headers=["Authorization", settings.PERSONA_ID_HEADER],
)
mcpapp.mount_http(mount_path="/mcp")


# ---------- REST-only routers ----------
app.include_router(keys_router)
app.include_router(generations_router)
app.include_router(manifest_router)
app.include_router(health_router)
app.include_router(twynity_router)