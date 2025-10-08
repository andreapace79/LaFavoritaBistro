from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Core & Config
from backend.core.config import settings
from backend.core.auth import (
    Token,
    UserOut,
    get_current_user,
    login_and_create_token,
    require_permissions,
    get_db,
)

# RBAC / Modules
from backend.core.rbac import crud as rbac_crud, schemas as rbac_schemas
from backend.core.rbac.models import Permission as PermissionModel  # alias chiaro
from backend.modules.users import crud as users_crud, schemas as users_schemas
from backend.modules.areas import crud as areas_crud, schemas as areas_schemas
from backend.modules.tables import crud as tables_crud, schemas as tables_schemas

# ---------------- App Setup ----------------
app = FastAPI(
    title="La Favorita Bistro – API",
    version="0.2.0",
    description="Backend gestionale per La Favorita Bistro – RBAC, aree, tavoli, comande, magazzino e moduli futuri.",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------- Middleware ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ in prod limitare al dominio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Routers ----------------
from backend.modules.users.router import router as users_router
app.include_router(users_router, prefix="/users", tags=["users"])
from backend.modules.admin.router import router as admin_router
app.include_router(admin_router)
from backend.modules.orders.router import router as orders_router
app.include_router(orders_router, prefix="/orders", tags=["orders"])


# ---------------- System ----------------
@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": getattr(settings, "PROJECT_NAME", "La Favorita Bistro")}


@app.get("/ping", tags=["system"])
def ping():
    return {"pong": True}


@app.get("/version", tags=["system"])
def version():
    return {"version": app.version, "project": getattr(settings, "PROJECT_NAME", "La Favorita Bistro")}


# ---------------- Auth ----------------
@app.post("/auth/login", response_model=Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_and_create_token(form_data, db)


@app.get("/me", response_model=UserOut, tags=["auth"])
def me(current_user=Depends(get_current_user)):
    return current_user


# ---------------- RBAC Example ----------------
@app.get("/areas", tags=["areas"], dependencies=[Depends(require_permissions("areas.manage"))])
def list_areas_example():
    return {"items": [], "note": "Questo è un placeholder protetto da RBAC."}


# ---------------- Dev Seed ----------------
@app.post("/dev/seed", tags=["dev"])
def dev_seed():
    """Popola dati base in ambiente di sviluppo"""
    from scripts.seed import seed_data
    from backend.core.config import settings

    # 🔒 Protezione: disabilitato in produzione
    if getattr(settings, "ENV", "development").lower() == "production":
        raise HTTPException(status_code=403, detail="Seed disabilitato in produzione")

    try:
        seed_data()
        return {"status": "ok", "message": "Seed completato con successo"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante il seed: {e}")


# ---------------- Entrypoint ----------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
