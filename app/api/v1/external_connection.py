# app/api/v1/external_connection.py
from fastapi import APIRouter

router = APIRouter(prefix="/external-connection", tags=["External Connection"])

@router.get("/")
async def list_connections():
    return []
