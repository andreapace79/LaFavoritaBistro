from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.db import get_db
from backend.core.rbac import crud, schemas
from backend.core.auth import get_password_hash
from backend.core.rbac.models import User

router = APIRouter()

@router.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_pw = get_password_hash(user.password)
    return crud.create_user(db, user.username, hashed_pw)

@router.get("/users/", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
