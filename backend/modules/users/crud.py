from sqlalchemy.orm import Session
from backend.modules.users import models, schemas
from backend.core.auth import get_password_hash

# ==========================================================
# CRUD Utenti
# ==========================================================
def get_user_by_username(db: Session, username: str):
    """Trova un utente per username"""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Crea un nuovo utente hashando la password"""
    hashed_pw = get_password_hash(user.password)
    db_user = models.User(username=user.username, password_hash=hashed_pw, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def list_users(db: Session):
    """Elenco completo degli utenti"""
    return db.query(models.User).all()
