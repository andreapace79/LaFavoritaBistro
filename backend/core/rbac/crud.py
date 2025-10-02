from sqlalchemy.orm import Session
from backend.core.rbac.models import User, Role, Permission

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, hashed_password: str):
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_role(db: Session, name: str):
    role = Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def create_permission(db: Session, code: str, description: str = ""):
    perm = Permission(code=code, description=description)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm
