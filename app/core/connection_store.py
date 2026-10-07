"""Encrypted MongoDB storage for Higgfield MCP.

Provides secure storage of credentials and secrets with strict user/persona pairing.
"""

from typing import Any, Optional

import motor.motor_asyncio
from cryptography.fernet import Fernet
from pydantic import BaseModel

from app.config import settings


class ConnectionData(BaseModel):
    """Data model for stored connections."""

    id: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    credential_key: Optional[str] = None  # Encrypted secret
    metadata: Optional[dict[str, Any]] = None


class ConnectionStore:
    """Thread-safe MongoDB storage with encryption."""

    def __init__(self) -> None:
        """Initialize MongoDB connection and encryption."""
        # Initialize MongoDB connection
        self._client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)
        self._db = self._client[settings.MONGODB_DB]
        self._collection = self._db["connections"]

        # Initialize encryption
        self._fernet = Fernet(settings.ENCRYPTION_KEY.encode() if isinstance(settings.ENCRYPTION_KEY, str) else settings.ENCRYPTION_KEY)

        # Ensure compound unique index on (user_id, persona_id)
        self._collection.create_index(
            [("user_id", 1), ("persona_id", 1)],
            unique=True,
        )

    async def save(self, connection_data: ConnectionData) -> ConnectionData:
        """Save or update connection with encryption.

        Args:
            connection_data: Connection data to save

        Returns:
            Saved connection data

        Raises:
            ValueError: If user_id or persona_id is missing
        """
        if not connection_data.user_id or not connection_data.persona_id:
            raise ValueError("user_id and persona_id are required for connection data")

        # Encrypt credential if present
        if connection_data.credential_key:
            encrypted = self._encrypt(connection_data.credential_key)
            connection_data.credential_key = encrypted

        # Use compound key for upsert
        doc_id = f"{connection_data.user_id}:{connection_data.persona_id}"

        await self._collection.update_one(
            {"_id": doc_id},
            {
                "$set": {
                    "user_id": connection_data.user_id,
                    "persona_id": connection_data.persona_id,
                    "name": connection_data.name,
                    "url": connection_data.url,
                    "credential_key": connection_data.credential_key,
                    "metadata": connection_data.metadata or {},
                }
            },
            upsert=True,
        )

        return connection_data

    async def get(self, user_id: str, persona_id: str) -> Optional[ConnectionData]:
        """Get connection by exact user/persona pair.

        Args:
            user_id: User identifier
            persona_id: Persona identifier

        Returns:
            Connection data or None if not found
        """
        doc_id = f"{user_id}:{persona_id}"
        doc = await self._collection.find_one({"_id": doc_id})

        if not doc:
            return None

        return ConnectionData(
            id=doc["_id"],
            name=doc.get("name"),
            url=doc.get("url"),
            credential_key=doc.get("credential_key"),
            metadata=doc.get("metadata"),
        )

    async def delete(self, user_id: str, persona_id: str) -> bool:
        """Delete connection by user/persona pair.

        Args:
            user_id: User identifier
            persona_id: Persona identifier

        Returns:
            True if deleted, False if not found
        """
        doc_id = f"{user_id}:{persona_id}"
        result = await self._collection.delete_one({"_id": doc_id})
        return result.deleted_count > 0

    async def list_by_user(self, user_id: str) -> list[ConnectionData]:
        """List all connections for a user.

        Args:
            user_id: User identifier

        Returns:
            List of connections
        """
        connections = []
        async for doc in self._collection.find({"user_id": user_id}).sort("name", 1):
            connections.append(
                ConnectionData(
                    id=doc["_id"],
                    name=doc.get("name"),
                    url=doc.get("url"),
                    credential_key=doc.get("credential_key"),  # Will be decrypted
                    metadata=doc.get("metadata"),
                )
            )
        return connections

    def _encrypt(self, data: str) -> str:
        """Encrypt data using Fernet."""
        return self._fernet.encrypt(data.encode()).decode()

    def _decrypt(self, encrypted_data: str) -> str:
        """Decrypt data using Fernet."""
        return self._fernet.decrypt(encrypted_data.encode()).decode()

    def public_metadata(self, connection_data: ConnectionData) -> dict[str, Any]:
        """Get public metadata without secrets.

        Args:
            connection_data: Connection data

        Returns:
            Dictionary with safe metadata fields
        """
        return {
            "id": connection_data.id,
            "name": connection_data.name,
            "url": connection_data.url,
            "has_credentials": connection_data.credential_key is not None,
            "metadata": connection_data.metadata or {},
        }


# Singleton instance
_store: Optional[ConnectionStore] = None


def get_connection_store() -> ConnectionStore:
    """Get singleton connection store instance."""
    global _store
    if _store is None:
        _store = ConnectionStore()
    return _store


async def get_db():
    """Get MongoDB connection for direct access."""
    store = get_connection_store()
    return store._client, store._collection