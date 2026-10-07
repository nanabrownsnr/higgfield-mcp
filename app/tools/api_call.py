"""MCP tool for making external API calls.

This tool allows the AI model to call external APIs using stored credentials.
"""

from typing import Any

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from app.config import settings
from app.core.connection_store import get_db

mcp = FastMCP("api_call")


class APICallInput(BaseModel):
    """Input model for API call tool."""

    url: str = Field(
        ...,
        description="URL of the external API endpoint",
    )
    method: str = Field(
        default="POST",
        description="HTTP method (GET, POST, PUT, DELETE)",
    )
    headers: dict[str, str] = Field(
        default={},
        description="Additional HTTP headers to include",
    )
    body: dict[str, Any] = Field(
        default={},
        description="Request body (for POST, PUT, PATCH)",
    )


@mcp.tool(
    name="call_external",
    description="Call an external API using stored API keys. Use this when you need to make requests to third-party services.",
    app_config={
        "visibility": ["model", "app"],
        "ui_resource_uri": "ui://api-call-result",
    },
)
async def call_external(
    input: APICallInput,
) -> dict[str, Any]:
    """Call an external API with authentication.

    This tool uses any stored API keys associated with the current user and persona
    to make authenticated requests to external services.

    Args:
        input: Parameters for the API call including URL, method, headers, and body

    Returns:
        Response from the external API

    Example for LLM use:
        - User asks to check a weather service API
        - I call this tool with service URL
        - Tool uses stored API keys if available

    Example for App UI use:
        - User triggers API call in UI
        - UI calls this tool with input parameters
        - Returns result for display
    """
    from app.core.license_server import license_watcher

    # Check license first
    license_status = await license_watcher.check_license()
    if not license_status["valid"]:
        return {
            "status": "error",
            "message": f"License validation failed: {license_status['error']}",
        }

    import httpx
    from jose import jwt
    from app.auth import TwynityIdentity
    from fastmcp.server.auth.context import get_mcp_context

    # Get context for user identification
    try:
        from fastmcp.server.auth.context import get_mcp_context

        context = get_mcp_context()
        # In MCP transport, credentials are passed via Authorization header
        # We'll use the context if available, otherwise use direct header parsing
        headers = {**input.headers, "Accept": "application/json"}

        # Make the API call
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.request(
                method=input.method,
                url=input.url,
                headers=headers,
                json=input.body,
            )

            return {
                "status": "success",
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": response.json() if response.headers.get("content-type") == "application/json" else response.text,
            }

    except httpx.TimeoutException:
        return {
            "status": "error",
            "message": "Request timed out",
        }
    except httpx.HTTPStatusError as e:
        return {
            "status": "error",
            "status_code": e.response.status_code,
            "message": f"API returned error: {e.response.text}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to make API call: {str(e)}",
        }


def register_tools(server: Server) -> None:
    """Register MCP tools with the server."""
    call_external.name = "call_external"
    call_external.description = "Call an external API using stored API keys"
    call_external.app_config = {
        "visibility": ["model", "app"],
        "ui_resource_uri": "ui://api-call-result",
    }

    server.tool(call_external)