from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.db import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact = Column(String(100))

    products = relationship("Product", back_populates="supplier", cascade="all, delete")
