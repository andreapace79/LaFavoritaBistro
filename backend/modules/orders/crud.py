from sqlalchemy.orm import Session
from backend.modules.orders.models import Order, OrderItem, OrderStatus
from backend.modules.orders.schemas import OrderCreate
from datetime import datetime


def list_orders(db: Session):
    return db.query(Order).order_by(Order.created_at.desc()).all()


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def create_order(db: Session, data: OrderCreate):
    order = Order(table_id=data.table_id, status=data.status)
    db.add(order)
    db.flush()  # per ottenere order.id prima del commit

    total = 0
    for item in data.items:
        db_item = OrderItem(order_id=order.id, name=item.name, quantity=item.quantity, price=item.price)
        total += item.quantity * item.price
        db.add(db_item)

    order.total = total
    db.commit()
    db.refresh(order)
    return order


def close_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if not order:
        return None
    order.status = OrderStatus.CLOSED
    order.closed_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    return order
