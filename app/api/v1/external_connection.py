# app/api/v1/external_connection.py
from fastapi import APIRouter, Depends
from app.core.authentication.auth_middleware import get_effective_owner_id
from app.core.storage import MongoStorage
from app.models.api_key import APIKey

router = APIRouter(prefix="/external-connection", tags=["External Connection"])

# Re‑use the same key storage as the key endpoint
key_storage = MongoStorage(model=APIKey, collection="api_keys", encrypted_fields=["key"])

@router.get("/me", response_model=list[APIKey])
async def my_keys(owner_id: str = Depends(get_effective_owner_id)):
    """Return only the keys belonging to the authenticated caller."""
    return await key_storage.list_for_owner(owner_id)

