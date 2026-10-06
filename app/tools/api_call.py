# app/tools/api_call.py
import httpx
from mcp.server import Server
from mcp.types import ToolResult
from pydantic import BaseModel
from typing import List
from fastapi import Depends, HTTPException
from app.core.authentication.auth_middleware import get_effective_owner_id
from app.core.storage import MongoStorage
from app.models.api_key import APIKey

# Storage for API keys
key_storage = MongoStorage(model=APIKey, collection="api_keys", encrypted_fields=["key"])

class CallRequest(BaseModel):
    target: str   # URL of the external service
    payload: dict = {}

class CallResponse(BaseModel):
    status: int
    body: dict


def register_tools(server: Server) -> None:

    @server.tool(
        visibility=["model", "app"],
        name="call_external",
        description="Calls an external API using a stored API key (POST).",
    )
    async def call_external(
        request: CallRequest,
        owner_id: str = Depends(get_effective_owner_id),
    ) -> ToolResult:
        keys = await key_storage.list_for_owner(owner_id)
        if not keys:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "No API key configured for this user")

        api_key = keys[0].key

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    request.target,
                    json=request.payload,
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=20,
                )
                resp.raise_for_status()
                return CallResponse(status=resp.status_code, body=resp.json())
            except httpx.HTTPStatusError as exc:
                return CallResponse(
                    status=exc.response.status_code,
                    body={"error": exc.response.text},
                )
            except Exception as exc:
                return CallResponse(
                    status=500,
                    body={"error": str(exc)},
                )
