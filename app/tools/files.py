"""MCP tool for file system operations.

Provides LLM and App UI with read/write access to owner's file directory.
"""

from pathlib import Path
from mcp.server import Server
from mcp.types import ToolResult
from pydantic import BaseModel, Field

from app.config import settings
from app.core.license_server import license_watcher

mcp = FastMCP("files")


FILE_ROOT = Path(__file__).resolve().parent.parent / "app" / "files"

# Ensure base path exists
FILE_ROOT.mkdir(parents=True, exist_ok=True)


def register_tools(server: Server) -> None:
    """Register file system tools with the server."""

    @server.tool(
        name="list_dir",
        description="List all files and subdirectories under the owner's file directory",
        app_config={
            "visibility": ["model", "app"],
            "ui_resource_uri": "ui://file-browser",
        },
    )
    async def list_dir(path: str = ".") -> ToolResult:
        """List directory contents.

        Args:
            path: Relative path from owner's file directory

        Returns:
            List of files and directories
        """
        # Get current user from context
        # In real implementation, use get_mcp_context() to get authenticated user
        owner_id = settings.SERVICE_ID  # Default to service ID in real use

        cwd = FILE_ROOT / owner_id / path
        cwd.mkdir(parents=True, exist_ok=True)

        items = []
        for p in cwd.iterdir():
            items.append({"name": p.name, "type": "dir" if p.is_dir() else "file"})

        return {"items": items, "path": str(cwd)}

    @server.tool(
        name="get_file",
        description="Return the contents of a file (as text or binary if image)",
        app_config={
            "visibility": ["model", "app"],
            "ui_resource_uri": "ui://file-viewer",
        },
    )
    async def get_file(path: str) -> ToolResult:
        """Get file contents.

        Args:
            path: Path to the file

        Returns:
            File contents as text or binary data

        Note:
            Images (PNG, JPG, JPEG, GIF) are returned as hex-encoded binary
        """
        # Get current user from context
        owner_id = settings.SERVICE_ID  # Default to service ID in real use

        fpath = (FILE_ROOT / owner_id / path).resolve()

        if not fpath.exists() or not fpath.is_file():
            return {"error": "not found", "path": path}

        if fpath.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}:
            # Return hex-encoded binary for images
            return {
                "contentType": "image" + fpath.suffix,
                "content": fpath.read_bytes().hex(),
            }
        else:
            return {"text": fpath.read_text(encoding="utf-8")}

    server.tool(list_dir)
    server.tool(get_file)