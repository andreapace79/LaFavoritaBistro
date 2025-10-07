from datetime import datetime, timedelta
from typing import Callable, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Import progetto
from backend.core.db import SessionLocal
from backend.core.config import settings
from backend.modules.users.models import User
from backend.core.rbac.models import Permission, user_roles, role_permissions

# ==========================================================
# Config & costanti
# ==========================================================
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# L’endpoint di login è /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ==========================================================
# Schemi Pydantic
# ==========================================================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None  # username


class UserOut(BaseModel):
    id: int
    username: str
    is_active: bool

    class Config:
        from_attributes = True


# ==========================================================
# DB dependency
# ==========================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================================
# Password helpers
# ==========================================================
def verify_password(plain_password: str, password_hash: str) -> bool:
    return bcrypt.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    return bcrypt.hash(password)


# ==========================================================
# JWT helpers
# ==========================================================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


# ==========================================================
# Login handler
# ==========================================================
def login_and_create_token(form_data: OAuth2PasswordRequestForm, db: Session) -> Token:
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # ⚠️ Usa password_hash dal modello
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return Token(access_token=token)


# ==========================================================
# Current user dependency
# ==========================================================
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user


# ==========================================================
# RBAC dependency: richiede permessi
# ==========================================================
def require_permissions(*required_codes: str) -> Callable:
    """
    Esempi:
        @app.get("/areas", dependencies=[Depends(require_permissions("areas.manage"))])
        @app.post("/users", dependencies=[Depends(require_permissions("users.write"))])
    """
    def dependency(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        if not required_codes:
            return

        # Prende i codici permesso dell'utente via ruoli
        q = (
            db.query(Permission.code)
              .join(role_permissions, role_permissions.c.permission_id == Permission.id)
              .join(user_roles, user_roles.c.role_id == role_permissions.c.role_id)
              .filter(user_roles.c.user_id == current_user.id)
        )
        user_perm_codes = {row[0] for row in q.all()}

        # wildcard concede tutto
        if "*" in user_perm_codes:
            return

        missing = [code for code in required_codes if code not in user_perm_codes]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permissions: {', '.join(missing)}",
            )
    return dependency
