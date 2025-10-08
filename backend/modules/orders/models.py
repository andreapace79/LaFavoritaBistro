from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum, func
from sqlalchemy.orm import relationship
from backend.core.db import Base
import enum


class OrderStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id", ondelete="SET NULL"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    status = Column(Enum(OrderStatus), default=OrderStatus.OPEN)
    total = Column(Float, default=0)
    created_at = Column(DateTime, default=func.now())
    closed_at = Column(DateTime, nullable=True)

    table = relationship("Table", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, default=0)

    order = relationship("Order", back_populates="items")
