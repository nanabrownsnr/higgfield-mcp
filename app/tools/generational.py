"""MCP tool for generation tracking.

Provides LLM and App UI with generation history and management.
"""

from typing import Any

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from app.config import settings
from app.core.connection_store import get_connection_store

mcp = FastMCP("generational")


class GenerationData(BaseModel):
    """Data model for generation records."""

    id: str
    content: str
    metadata: dict[str, Any] = {}
    created_at: str | None = None


def register_tools(server: Server) -> None:
    """Register generation tools with the server."""

    @server.tool(
        name="list_generations",
        description="List all generations created by the current user",
        app_config={
            "visibility": ["model", "app"],
            "ui_resource_uri": "ui://generation-history",
        },
    )
    async def list_generations() -> dict[str, Any]:
        """List generation history.

        Returns:
            List of generations with metadata
        """
        # Get current user from context
        from fastmcp.server.auth.context import get_mcp_context

        try:
            context = get_mcp_context()
            # In production, use context.user_id and context.persona_id
            user_id = context.user_id if hasattr(context, "user_id") else settings.SERVICE_ID
        except Exception:
            user_id = settings.SERVICE_ID

        # Get connection store
        store = get_connection_store()
        connections = await store.list_by_user(user_id)

        generations = []
        for conn in connections:
            generations.append(
                {
                    "name": conn.name,
                    "url": conn.url,
                    "created_at": conn.metadata.get("created_at") if conn.metadata else None,
                    "metadata": conn.metadata,
                }
            )

        return {
            "generations": generations,
            "count": len(generations),
        }

    @server.tool(
        name="create_generation",
        description="Create a new generation record",
        app_config={
            "visibility": ["model", "app"],
            "ui_resource_uri": "ui://generation-creator",
        },
    )
    async def create_generation(name: str, content: str, metadata: dict[str, Any] = None) -> dict[str, Any]:
        """Create a new generation record.

        Args:
            name: Generation name
            content: Generation content
            metadata: Additional metadata

        Returns:
            Created generation record
        """
        from fastmcp.server.auth.context import get_mcp_context

        try:
            context = get_mcp_context()
            user_id = context.user_id if hasattr(context, "user_id") else settings.SERVICE_ID
        except Exception:
            user_id = settings.SERVICE_ID

        # Get connection store
        store = get_connection_store()

        # Get or create persona-based connection
        # In production, use context.persona_id
        persona_id = "default"

        connection_data = store.public_metadata(
            GenerationData(
                id=name,
                content=content,
                metadata={"created_at": None, **(metadata or {})},
            )
        )

        await store.save(
            store.__class__(  # noqa: SLF001
                user_id=user_id,
                persona_id=persona_id,
                name=name,
                url=f"generation://{name}",
                credential_key=None,
                metadata={"created_at": None, **(metadata or {})},
            )
        )

        return {
            "status": "success",
            "generation": {
                "name": name,
                "content": content,
                "metadata": metadata,
            },
        }

    server.tool(list_generations)
    server.tool(create_generation)