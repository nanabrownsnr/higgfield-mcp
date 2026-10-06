# app/core/authentication/role.py
from fastapi import Depends, HTTPException, status
from fastapi import Depends, HTTPException, status
from app.core.authentication.auth_middleware import get_current_token, TokenData

class RoleBasedAccessControl:
    def __init__(self, roles: list[str]):
        self.allowed_roles = roles

    def __call__(self, current_token: TokenData = Depends(get_current_token)):
        if current_token.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User role not permitted to perform this action",
            )
# Predefined role guards
allow_resource_admin = RoleBasedAccessControl(["admin", "super_admin"])
