# app/core/storage.py
from typing import Generic, TypeVar
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from app.config import settings
from app.core.encryption import encrypt_data, decrypt_data

T = TypeVar("T", bound=BaseModel)

class MongoStorage(Generic[T]):
    def __init__(self, model: type[T], collection: str, encrypted_fields: list[str]):
        client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = client[settings.MONGODB_DB]
        self.collection = self.db[collection]
        self.model = model
        self.encrypted_fields = encrypted_fields

    async def create(self, owner_id: str, data: dict) -> T:
        doc = {"owner_id": owner_id, **data}
        for f in self.encrypted_fields:
            if f in doc:
                doc[f] = encrypt_data(doc[f])
        result = await self.collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return self._to_model(doc)

    async def list_for_owner(self, owner_id: str) -> list[T]:
        cursor = self.collection.find({"owner_id": owner_id})
        return [self._to_model(d) async for d in cursor]

    def _to_model(self, doc) -> T:
        for f in self.encrypted_fields:
            if f in doc:
                doc[f] = decrypt_data(doc[f])
        return self.model(**doc)