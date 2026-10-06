# app/api/v1/manifest.py
from fastapi import APIRouter

router = APIRouter(prefix="/manifest", tags=["Manifest"])

@router.get("/mcp.json")
async def get_manifest():
    return {"service": "example"}
