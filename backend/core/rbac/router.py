from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.core.rbac import crud, schemas
from backend.core.auth import get_password_hash

router = APIRouter(
    prefix="/rbac/users",
    tags=["Users"],
)

@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pw = get_password_hash(user.password)
    db_user = crud.create_user(db, user.username, hashed_pw)
    return db_user


@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


# ✅ Endpoint aggiornamento utente
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # aggiorno i campi
    db_user.username = user.username
    if user.password:
        db_user.hashed_password = get_password_hash(user.password)

    db.commit()
    db.refresh(db_user)
    return db_user
