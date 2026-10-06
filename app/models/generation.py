# app/models/generation.py
from pydantic import BaseModel

class Generation(BaseModel):
    id: str
    name: str
    metadata: dict | None = None
