from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.db import Base

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    tables = relationship("Table", back_populates="area", cascade="all, delete")
