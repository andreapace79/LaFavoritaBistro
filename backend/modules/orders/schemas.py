from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from enum import Enum


class OrderStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class OrderItemBase(BaseModel):
    name: str
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemOut(OrderItemBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    table_id: int
    status: OrderStatus = OrderStatus.OPEN


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderOut(OrderBase):
    id: int
    total: float
    created_at: datetime
    closed_at: Optional[datetime]
    items: List[OrderItemOut]

    class Config:
        orm_mode = True
