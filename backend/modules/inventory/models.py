from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.db import Base
import datetime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=False)
    stock_qty = Column(Float, default=0.0)

    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    supplier = relationship("Supplier", back_populates="products")
    stock_moves = relationship("StockMove", back_populates="product", cascade="all, delete")


class StockMove(Base):
    __tablename__ = "stock_moves"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    qty = Column(Float, nullable=False)
    type = Column(String(10), nullable=False)  # in/out/adjust
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    product = relationship("Product", back_populates="stock_moves")
