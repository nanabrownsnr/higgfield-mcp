# app/models/api_key.py
from pydantic import BaseModel, Field
from typing import Optional

class APIKey(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    key: str
    owner_id: str
