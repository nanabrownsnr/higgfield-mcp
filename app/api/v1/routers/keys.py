# app/api/v1/routers/keys.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.authentication.auth_middleware import (
    get_current_token,
    get_effective_owner_id,
)
from app.core.authentication.role import allow_resource_admin
from app.core.storage import MongoStorage
from app.models.api_key import APIKey

router = APIRouter(prefix="/keys", tags=["API Keys"])

storage = MongoStorage(model=APIKey, collection="api_keys", encrypted_fields=["key"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_api_key(
    data: APIKey,
    owner_id: str = Depends(get_effective_owner_id),
    _auth: None = Depends(allow_resource_admin),
):
    key = APIKey(name=data.name, key=data.key, owner_id=owner_id)
    await storage.create(owner_id, key.dict(exclude={"owner_id"}))
    return {"status": "created", "name": key.name}

@router.get("/", response_model=List[APIKey])
async def list_api_keys(
    owner_id: str = Depends(get_effective_owner_id),
):
    return await storage.list_for_owner(owner_id)
