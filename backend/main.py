from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from core.auth import (
    Token,
    UserOut,
    get_current_user,
    login_and_create_token,
    require_permissions,
    get_db,
)
from core.config import settings


app = FastAPI(
    title="La Favorita Bistro – API",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ==========================================================
# Health check
# ==========================================================
@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


# ==========================================================
# Auth: /auth/login (OAuth2 password flow)
# ==========================================================
@app.post("/auth/login", response_model=Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Esegui login con username/password (form-url-encoded).
    Restituisce un JWT da usare come Bearer token.
    """
    return login_and_create_token(form_data, db)


# ==========================================================
# Who am I
# ==========================================================
@app.get("/me", response_model=UserOut, tags=["auth"])
def me(current_user=Depends(get_current_user)):
    return current_user


# ==========================================================
# Esempio endpoint protetto da permesso RBAC
# ==========================================================
@app.get("/areas", tags=["areas"], dependencies=[Depends(require_permissions("areas.manage"))])
def list_areas_example():
    """
    Esempio di endpoint che richiede il permesso 'areas.manage'.
    Sostituisci con l'implementazione reale nel modulo Aree.
    """
    return {"items": [], "note": "Questo è un placeholder protetto da RBAC."}
