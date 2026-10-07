"""MCP tool for content rendering.

Provides LLM and App UI with formatted content display.
"""

from mcp.server import Server
from mcp.types import ToolResult
from pydantic import BaseModel, Field

mcp = FastMCP("render_content")


class RenderInput(BaseModel):
    """Input model for render tool."""

    content_type: str = Field(
        default="text",
        description="Type of content to render (text, html, json)"
    )
    content: str = Field(
        ...,
        description="Content to render"
    )
    format_options: dict[str, Any] = Field(
        default={},
        description="Additional formatting options"
    )


def register_tools(server: Server) -> None:
    """Register rendering tools with the server."""

    @server.tool(
        name="render_output",
        description="Render content for display in the UI, supporting HTML and formatted text",
        app_config={
            "visibility": ["model", "app"],
            "ui_resource_uri": "ui://content-renderer",
        },
    )
    async def render_output(input: RenderInput) -> ToolResult:
        """Render content for UI display.

        Args:
            input: Content to render with type and formatting options

        Returns:
            Rendered content with metadata
        """
        result = {
            "type": input.content_type,
            "content": input.content,
            "formatted": False,
            "warnings": [],
        }

        # Add content type header for images
        if input.content_type == "image":
            import base64

            # Check if content is already base64 or plain hex
            try:
                decoded = base64.b64decode(input.content)
                result["content"] = "data:image/png;base64," + base64.b64encode(decoded).decode()
            except Exception:
                # Assume hex encoded
                try:
                    decoded_bytes = bytes.fromhex(input.content)
                    result["content"] = "data:image/png;base64," + base64.b64encode(decoded_bytes).decode()
                except Exception:
                    result["warnings"].append("Could not decode image content")

        # Format JSON content
        elif input.content_type == "json":
            import json

            try:
                data = json.loads(input.content)
                result["formatted"] = True
                result["pretty_json"] = json.dumps(data, indent=2)
            except json.JSONDecodeError:
                result["warnings"].append("Invalid JSON content")

        # Check for HTML content
        if "<html" in input.content.lower() or "<body" in input.content.lower():
            result["content_type"] = "html"

        return result

    server.tool(render_output)