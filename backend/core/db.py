from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings  # deve avere DATABASE_URL

# Base comune a tutti i moduli
Base = declarative_base()

# Engine + Session
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Funzione utility
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


