from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

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
from backend.modules.users import crud as users_crud, schemas as users_schemas
from backend.modules.areas import crud as areas_crud, schemas as areas_schemas
from backend.modules.tables import crud as tables_crud, schemas as tables_schemas

app = FastAPI(
    title="La Favorita Bistro – API",
    version="0.2.0",
    description="Backend gestionale per La Favorita Bistro – RBAC, aree, tavoli, comande, magazzino e moduli futuri.",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod: limita al dominio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from backend.modules.users.router import router as users_router
app.include_router(users_router, prefix="/users", tags=["users"])

# ---------------- System ----------------
@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": getattr(settings, "PROJECT_NAME", "La Favorita Bistro")}

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
def dev_seed(db: Session = Depends(get_db)):
    """Popola dati base in ambiente di sviluppo"""
    if getattr(settings, "ENV", "development").lower() == "production":
        raise HTTPException(status_code=403, detail="Seed disabilitato in ambiente di produzione")

    try:
        # 1️⃣ Permessi base
        base_permissions = [
            {"name": "users.manage", "description": "Gestione utenti e ruoli"},
            {"name": "areas.manage", "description": "Gestione aree e layout"},
            {"name": "tables.manage", "description": "Gestione tavoli"},
            {"name": "inventory.read", "description": "Visualizza magazzino"},
            {"name": "inventory.write", "description": "Aggiorna magazzino"},
            {"name": "orders.manage", "description": "Gestione comande"},
            {"name": "reports.view", "description": "Visualizza report e KPI"},
        ]

        for perm in base_permissions:
            if not db.query(Permission).filter(Permission.name == perm["name"]).first():
                db.add(Permission(name=perm["name"], description=perm["description"]))
        db.commit()

        # 2️⃣ Utente admin
        from backend.modules.users import crud as users_crud, schemas as users_schemas
        user = users_crud.get_user_by_username(db, "admin")
        if not user:
            user = users_crud.create_user(
                db, users_schemas.UserCreate(username="admin", password="admin")
            )

        # 3️⃣ Ruolo admin con tutti i permessi
        from backend.core.rbac import crud as rbac_crud, schemas as rbac_schemas
        role = rbac_crud.get_role_by_name(db, "admin")
        if not role:
            all_permissions = [p.name for p in db.query(Permission).all()]
            role = rbac_crud.create_role(
                db,
                rbac_schemas.RoleCreate(
                    name="admin",
                    description="Amministratore di sistema",
                    permissions=all_permissions,
                ),
            )
        rbac_crud.assign_role_to_user(db, user.id, role.id)

        # 4️⃣ Area e tavoli di esempio
        from backend.modules.areas import crud as areas_crud, schemas as areas_schemas
        from backend.modules.tables import crud as tables_crud, schemas as tables_schemas

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
            "created_or_existing": {
                "user": user.username,
                "role": role.name,
                "permissions": [p["name"] for p in base_permissions],
                "area": area.name,
                "tables": ["T1", "T2"],
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- Misc ----------------
@app.get("/ping", tags=["system"])
def ping():
    return {"pong": True}

@app.get("/version", tags=["system"])
def version():
    return {"version": app.version, "project": getattr(settings, "PROJECT_NAME", "La Favorita Bistro")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
