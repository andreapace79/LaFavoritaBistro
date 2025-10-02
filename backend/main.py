from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.db import Base, engine
from backend.core.rbac.router import router as rbac_router

app = FastAPI(title="La Favorita Bistro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inizializza DB
Base.metadata.create_all(bind=engine)

@app.get("/ping")
def ping():
    return {"status": "ok"}

# Routers
app.include_router(rbac_router, prefix="/rbac", tags=["rbac"])
