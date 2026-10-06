# app/tools/files.py
import os
from pathlib import Path
from mcp.server import Server
from mcp.types import ToolResult
from fastapi import Depends
from app.core.authentication.auth_middleware import get_effective_owner_id

FILE_ROOT = Path(__file__).resolve().parent.parent / "app" / "files"

# Ensure base path exists
FILE_ROOT.mkdir(parents=True, exist_ok=True)


def register_tools(server: Server) -> None:
    @server.tool(
        name="list_dir",
        description="List all files and subdirectories under the owner's folder",
        visibility=["model", "app"],
    )
    async def list_dir(
        path: str = ".",
        owner_id: str = Depends(get_effective_owner_id),
    ) -> ToolResult:
        cwd = FILE_ROOT / owner_id / path
        cwd.mkdir(parents=True, exist_ok=True)
        items = []
        for p in cwd.iterdir():
            items.append({"name": p.name, "type": "dir" if p.is_dir() else "file"})
        return {"items": items}

    @server.tool(
        name="get_file",
        description="Return the contents of a file (as text or binary if image)",
        visibility=["model", "app"],
    )
    async def get_file(
        path: str,
        owner_id: str = Depends(get_effective_owner_id),
    ) -> ToolResult:
        fpath = (FILE_ROOT / owner_id / path).resolve()
        if not fpath.exists() or not fpath.is_file():
            return {"error": "not found"}
        if fpath.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}:
            # Return base64‑like string for binary image
            return {
                "contentType": "image" + fpath.suffix,
                "content": fpath.read_bytes().hex(),
            }
        else:
            return {"text": fpath.read_text(encoding="utf-8")}
