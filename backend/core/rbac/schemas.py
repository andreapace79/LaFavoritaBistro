from pydantic import BaseModel
from typing import List, Optional

class PermissionRead(BaseModel):
    id: int
    code: str
    description: Optional[str] = None
    class Config: orm_mode = True

class RoleRead(BaseModel):
    id: int
    name: str
    permissions: List[PermissionRead] = []
    class Config: orm_mode = True

class UserRead(BaseModel):
    id: int
    username: str
    roles: List[RoleRead] = []
    class Config: orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str
