from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    area_id = Column(Integer, ForeignKey("areas.id"))

    area = relationship("Area", back_populates="tables")
