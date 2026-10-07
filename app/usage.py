"""Usage tracking middleware for Higgfield MCP.

This module provides fire-and-forget usage reporting for authenticated endpoints.
"""

from datetime import UTC, datetime

from starlette.requests import Request

from app.config import settings


async def track_usage(request: Request) -> None:
    """Capture usage metrics and send to the reporting endpoint.

    This runs asynchronously and doesn't block the response.
    Args:
        request: The request being processed

    Note:
        Only tracks requests with Authorization header to avoid tracking unauthenticated traffic.
    """
    if "Authorization" not in request.headers:
        return

    try:
        data = {
            "service": settings.APP_TITLE,
            "method": request.method,
            "endpoint": str(request.url),
            "timestamp": datetime.now(UTC).timestamp(),
            "ip_address": request.client.host if request.client else None,
        }

        import httpx

        async with httpx.AsyncClient(timeout=5) as client:
            await client.post(settings.USAGE_REPORT_ENDPOINT, json=data, timeout=5)
    except Exception:
        # Log error if reporting fails, but don't fail the request
        # In production, this should log to structured logging
        pass