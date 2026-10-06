# app/api/v1/routers/generations.py
from fastapi import APIRouter, Depends
from typing import List
from app.core.authentication.auth_middleware import get_effective_owner_id
from app.core.storage import MongoStorage
from app.models.generation import Generation

router = APIRouter(prefix="/generations", tags=["Generations"])

storage = MongoStorage(model=Generation, collection="generations", encrypted_fields=[])

@router.get("/", response_model=List[Generation])
async def list_generations(owner_id: str = Depends(get_effective_owner_id)):
    return await storage.list_for_owner(owner_id)

@router.post("/", response_model=Generation)
async def create_generation(gen: Generation, owner_id: str = Depends(get_effective_owner_id)):
    # ignore gen.id from client; create new Mongo ID
    data = gen.dict(exclude_unset=True)
    data.pop("id", None)
    return await storage.create(owner_id, data)
