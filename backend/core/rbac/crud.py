from sqlalchemy.orm import Session
from backend.core.rbac import models

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, username: str, hashed_password: str):
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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
