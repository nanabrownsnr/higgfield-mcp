"""MCP tools package for Higgfield MCP."""

from app.tools.api_call import register_tools as register_api_tools
from app.tools.files import register_tools as register_files_tools
from app.tools.generational import register_tools as register_gen_tools
from app.tools.render_content import register_tools as register_render_tools


def register_tools(server):
    """Register all tools with the server."""
    register_api_tools(server)
    register_files_tools(server)
    register_gen_tools(server)
    register_render_tools(server)