# app/tools/generational.py
from mcp.server import Server
from mcp.types import ToolResult
from fastapi import Depends
from app.core.authentication.auth_middleware import get_effective_owner_id
from app.core.storage import MongoStorage
from app.models.generation import Generation

generation_storage = MongoStorage(model=Generation, collection="generations", encrypted_fields=[])

def register_tools(server: Server) -> None:
    @server.tool(
        name="list_generations",
        description="Return a list of all generations the owner has created",
        visibility=["model", "app"],
    )
    async def list_generations(owner_id: str = Depends(get_effective_owner_id)) -> ToolResult:
        gens = await generation_storage.list_for_owner(owner_id)
        return {"generations": [g.dict() for g in gens]}
