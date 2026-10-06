# app/core/authentication/auth_token.py
from pydantic import BaseModel

class TokenData(BaseModel):
    sub: str | None = None
    role: str | None = None
