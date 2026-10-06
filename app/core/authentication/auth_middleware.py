# app/core/authentication/auth_middleware.py
from fastapi import Depends, HTTPException, Request, status
from app.config import settings
from app.core.authentication.auth_token import TokenData
from jose import jwt

async def get_current_token(request: Request) -> TokenData:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    token = auth_header[7:]
    try:
        payload = jwt.decode(token, options={"verify_signature": False, "verify_aud": False})
    except Exception as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    return TokenData(sub=payload.get("sub"), role=payload.get("role"))

async def get_effective_owner_id(
    request: Request,
    token: TokenData = Depends(get_current_token),
) -> str:
    persona_id = request.headers.get(settings.PERSONA_ID_HEADER)
    return persona_id or token.sub
