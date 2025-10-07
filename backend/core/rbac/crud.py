# backend/core/rbac/crud.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.core.rbac.models import Role, Permission, user_roles, role_permissions
from backend.core.rbac import schemas

# --- Roles ---
def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    return db.execute(select(Role).where(Role.name == name)).scalar_one_or_none()

def create_role(db: Session, role_in: schemas.RoleCreate) -> Role:
    role = Role(name=role_in.name, description=role_in.description or "")
    db.add(role)
    db.flush()  # per avere role.id

    # crea eventuali permissions dal codice
    for code in role_in.permissions:
        perm = get_permission_by_code(db, code)
        if not perm:
            perm = create_permission(db, schemas.PermissionCreate(code=code, description="wildcard" if code == "*" else None))
        db.execute(role_permissions.insert().values(role_id=role.id, permission_id=perm.id))

    db.commit()
    db.refresh(role)
    return role

def assign_role_to_user(db: Session, user_id: int, role_id: int) -> None:
    db.execute(user_roles.insert().values(user_id=user_id, role_id=role_id))
    db.commit()

# --- Permissions ---
def get_permission_by_code(db: Session, code: str) -> Optional[Permission]:
    return db.execute(select(Permission).where(Permission.code == code)).scalar_one_or_none()

def create_permission(db: Session, perm_in: schemas.PermissionCreate) -> Permission:
    perm = Permission(code=perm_in.code, description=perm_in.description or "")
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm
