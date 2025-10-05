from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from backend.core.db import Base

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    # Dati liberi per layout (posizioni, note, ecc.)
    layout_meta = Column(JSON, nullable=True)

    # Tavoli collegati; cascade su delete area
    tables = relationship(
        "Table",
        back_populates="area",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

