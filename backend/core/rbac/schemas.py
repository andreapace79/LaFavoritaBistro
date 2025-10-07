# backend/core/rbac/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permissions: List[str] = []

class RoleOut(RoleBase):
    id: int
    class Config:
        from_attributes = True

class PermissionBase(BaseModel):
    code: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionOut(PermissionBase):
    id: int
    class Config:
        from_attributes = True

