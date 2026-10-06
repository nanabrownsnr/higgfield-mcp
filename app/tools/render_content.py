# app/tools/render_content.py
from mcp.server import Server
from mcp.types import ToolResult
from fastapi import Depends
from app.core.authentication.auth_middleware import get_effective_owner_id
from app.tools.files import get_file

def register_tools(server: Server) -> None:
    @server.tool(
        name="render_output",
        description="Return an image or text payload for display in the MCP App UI",
        visibility=["model", "app"],
    )
    async def render_output(
        path: str,
        owner_id: str = Depends(get_effective_owner_id),
    ) -> ToolResult:
        return await get_file(path, owner_id)
