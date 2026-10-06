# app/ui/file_dir/resource.py
from mcp.server import Server
from mcp.types import Resource

SERVER = Server()

@Resource(resource_uri="ui://file_dir/index.html")
def get_ui_resource() -> None:
    # The actual UI index.html lives in the same directory
    pass
