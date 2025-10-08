# backend/modules/admin/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.auth import get_db, require_permissions
from backend.modules.admin import crud, schemas

router = APIRouter(prefix="/admin", tags=["admin"])


# === USERS ===
@router.get("/users", response_model=list[schemas.UserOut], dependencies=[Depends(require_permissions("users.manage"))])
def list_users(db: Session = Depends(get_db)):
    users = crud.list_users(db)
    return [
        schemas.UserOut(
            id=u.id, username=u.username, is_active=u.is_active, roles=crud.get_user_roles(db, u.id)
        )
        for u in users
    ]


@router.post("/users", response_model=schemas.UserOut, dependencies=[Depends(require_permissions("users.manage"))])
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(crud.User).filter(crud.User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username già esistente")
    user = crud.create_user(db, data.username, data.password, data.roles or [])
    return schemas.UserOut(
        id=user.id, username=user.username, is_active=user.is_active, roles=crud.get_user_roles(db, user.id)
    )


# === ROLES ===
@router.get("/roles", response_model=list[schemas.RoleOut], dependencies=[Depends(require_permissions("users.manage"))])
def list_roles(db: Session = Depends(get_db)):
    roles = crud.list_roles(db)
    return [
        schemas.RoleOut(
            id=r.id,
            name=r.name,
            description=r.description,
            permissions=crud.get_role_permissions(db, r.id),
        )
        for r in roles
    ]


@router.post("/roles", response_model=schemas.RoleOut, dependencies=[Depends(require_permissions("users.manage"))])
def create_role(data: schemas.RoleCreate, db: Session = Depends(get_db)):
    role = crud.create_role(db, data.name, data.description or "", data.permissions or [])
    return schemas.RoleOut(
        id=role.id,
        name=role.name,
        description=role.description,
        permissions=crud.get_role_permissions(db, role.id),
    )


# === PERMISSIONS ===
@router.get("/permissions", response_model=list[schemas.PermissionOut], dependencies=[Depends(require_permissions("users.manage"))])
def list_permissions(db: Session = Depends(get_db)):
    return crud.list_permissions(db)
