from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Core imports
from backend.core.config import settings
from backend.core.auth import (
    Token,
    UserOut,
    get_current_user,
    login_and_create_token,
    require_permissions,
    get_db,
    get_password_hash,
)

# RBAC / Modules
from backend.core.rbac import crud as rbac_crud, schemas as rbac_schemas
from backend.modules.areas import crud as areas_crud, schemas as areas_schemas
from backend.modules.tables import crud as tables_crud, schemas as tables_schemas

# ==========================================================
# App setup
# ==========================================================
app = FastAPI(
    title="La Favorita Bistro – API",
    version="0.2.0",
    description="Backend gestionale per La Favorita Bistro – RBAC, aree, tavoli, comande, magazzino e più moduli futuri.",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS (per comunicazione col frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione specificare il dominio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import router dopo la creazione dell’app
from backend.modules.users.router import router as users_router
app.include_router(users_router, prefix="/users", tags=["users"])

# ==========================================================
# Health check
# ==========================================================
@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": settings.PROJECT_NAME}

# ==========================================================
# AUTH
# ==========================================================
@app.post("/auth/login", response_model=Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Esegui login con username/password."""
    return login_and_create_token(form_data, db)


@app.get("/me", response_model=UserOut, tags=["auth"])
def me(current_user=Depends(get_current_user)):
    """Restituisce i dati dell’utente autenticato"""
    return current_user


# ==========================================================
# RBAC Example
# ==========================================================
@app.get("/areas", tags=["areas"], dependencies=[Depends(require_permissions("areas.manage"))])
def list_areas_example():
    """Esempio di endpoint protetto da permesso RBAC"""
    return {"items": [], "note": "Questo è un placeholder protetto da RBAC."}


# ==========================================================
# DEV SEED – Inizializzazione ambiente di sviluppo
# ==========================================================
@app.post("/dev/seed", tags=["dev"])
def dev_seed(db: Session = Depends(get_db)):
    """Popola dati base in ambiente di sviluppo"""
    if getattr(settings, "ENV", "development").lower() == "production":
        raise HTTPException(status_code=403, detail="Seed disabilitato in ambiente di produzione")

    try:
        # 1️⃣ Utente admin
        from backend.modules.users import crud as users_crud, schemas as users_schemas
        user = users_crud.get_user_by_username(db, "admin")
        if not user:
            hashed_pw = get_password_hash("admin")
            user = users_crud.create_user(
                db, users_schemas.UserCreate(username="admin", password=hashed_pw)
            )

        # 2️⃣ Ruolo admin
        role = rbac_crud.get_role_by_name(db, "admin")
        if not role:
            role = rbac_crud.create_role(
                db,
                rbac_schemas.RoleCreate(
                    name="admin",
                    description="Amministratore con tutti i permessi",
                    permissions=["*"],
                ),
            )
            rbac_crud.assign_role_to_user(db, user.id, role.id)

        # 3️⃣ Area e tavoli di esempio
        area = areas_crud.get_area_by_name(db, "Interno")
        if not area:
            area = areas_crud.create_area(
                db,
                areas_schemas.AreaCreate(
                    name="Interno",
                    layout_meta={"note": "Area principale interna"},
                ),
            )

        tables = tables_crud.list_tables_by_area(db, area.id)
        if not tables:
            tables_crud.create_table(db, tables_schemas.TableCreate(area_id=area.id, name="T1", seats=4))
            tables_crud.create_table(db, tables_schemas.TableCreate(area_id=area.id, name="T2", seats=2))

        return {
            "status": "ok",
            "created": {
                "user": user.username,
                "role": role.name,
                "area": area.name,
                "tables": ["T1", "T2"],
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================================
# Placeholder future modules
# ==========================================================
@app.get("/ping", tags=["system"])
def ping():
    return {"pong": True}


@app.get("/version", tags=["system"])
def version():
    return {"version": app.version, "project": settings.PROJECT_NAME}


# ==========================================================
# Entrypoint
# ==========================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
