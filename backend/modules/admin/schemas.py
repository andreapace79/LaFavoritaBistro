# backend/modules/admin/schemas.py
from pydantic import BaseModel
from typing import List, Optional


# --- Permissions ---
class PermissionBase(BaseModel):
    code: str
    description: Optional[str] = None


class PermissionOut(PermissionBase):
    id: int
    class Config:
        from_attributes = True


# --- Roles ---
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    permissions: Optional[List[str]] = []  # list of permission codes


class RoleOut(RoleBase):
    id: int
    permissions: List[str] = []
    class Config:
        from_attributes = True


# --- Users ---
class UserBase(BaseModel):
    username: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str
    roles: Optional[List[str]] = []  # list of role names


class UserOut(UserBase):
    id: int
    roles: List[str] = []
    class Config:
        from_attributes = True
