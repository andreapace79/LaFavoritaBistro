# backend/modules/admin/crud.py
from sqlalchemy.orm import Session
from backend.modules.users.models import User
from backend.core.rbac.models import Role, Permission, user_roles, role_permissions
from passlib.hash import bcrypt


# --- USERS ---
def list_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, username: str, password: str, roles: list[str]):
    user = User(username=username, password_hash=bcrypt.hash(password), is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)

    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if role:
            db.execute(user_roles.insert().values(user_id=user.id, role_id=role.id))
    db.commit()
    return user


def get_user_roles(db: Session, user_id: int):
    q = (
        db.query(Role.name)
        .join(user_roles, user_roles.c.role_id == Role.id)
        .filter(user_roles.c.user_id == user_id)
    )
    return [r[0] for r in q.all()]


# --- ROLES ---
def list_roles(db: Session):
    return db.query(Role).all()


def create_role(db: Session, name: str, description: str, permissions: list[str]):
    role = Role(name=name, description=description)
    db.add(role)
    db.commit()
    db.refresh(role)

    for code in permissions:
        perm = db.query(Permission).filter(Permission.code == code).first()
        if perm:
            db.execute(role_permissions.insert().values(role_id=role.id, permission_id=perm.id))
    db.commit()
    return role


def get_role_permissions(db: Session, role_id: int):
    q = (
        db.query(Permission.code)
        .join(role_permissions, role_permissions.c.permission_id == Permission.id)
        .filter(role_permissions.c.role_id == role_id)
    )
    return [r[0] for r in q.all()]


# --- PERMISSIONS ---
def list_permissions(db: Session):
    return db.query(Permission).all()
