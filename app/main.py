# app/main.py
import asyncio
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from fastapi import Request, HTTPException

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi_mcp import FastApiMCP
from mcp.server import Server
import httpx

from app.config import settings
from app.core.license_server import license_watcher
from app.tools.generational import register_tools as register_gen_tools
from app.tools.files import register_tools as register_files_tools
from app.tools.render_content import register_tools as register_render_tools
from app.api.v1.manifest import router as manifest_router
from app.api.v1.health import router as health_router
from app.api.v1.external_connection import router as external_connection_router

# ---------- Usage tracking ----------
async def track_usage(request: Request) -> None:
    if "Authorization" not in request.headers:
        return
    data = {
        "service": settings.APP_TITLE,
        "method": request.method,
        "endpoint": str(request.url),
        "timestamp": datetime.now(UTC).timestamp(),
        "ip_address": request.client.host,
    }
    async with httpx.AsyncClient() as client:
        await client.post(settings.USAGE_REPORT_ENDPOINT, json=data)

# ---------- FastAPI ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(license_watcher())
    yield

app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan, root_path=settings.ROOT_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def usage_middleware(request: Request, call_next):
    asyncio.create_task(track_usage(request))
    return await call_next(request)

@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    return RedirectResponse(url=f"{settings.ROOT_PATH}/docs")

# ---------- MCP tool routers ----------
register_tools(Server(app))
register_gen_tools(Server(app))
register_files_tools(Server(app))
register_render_tools(Server(app))

# ---------- MCP server ----------
mcpapp = FastApiMCP(app, headers=["Authorization", settings.PERSONA_ID_HEADER])
mcpapp.mount_http(mount_path="/mcp")

# ---------- REST-only routers ----------
app.include_router(keys_router)
app.include_router(generations_router)
app.include_router(manifest_router)
app.include_router(health_router)
app.include_router(external_connection_router)
# Note: Add manifest, health, external_connection, keys, etc. using the starter pattern
