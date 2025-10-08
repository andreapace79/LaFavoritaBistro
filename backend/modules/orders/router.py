from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.auth import get_db, require_permissions
from backend.modules.orders import crud, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.OrderOut], dependencies=[Depends(require_permissions("orders.manage"))])
def list_orders(db: Session = Depends(get_db)):
    return crud.list_orders(db)


@router.get("/{order_id}", response_model=schemas.OrderOut, dependencies=[Depends(require_permissions("orders.manage"))])
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Comanda non trovata")
    return order


@router.post("/", response_model=schemas.OrderOut, dependencies=[Depends(require_permissions("orders.manage"))])
def create_order(data: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, data)


@router.put("/{order_id}/close", response_model=schemas.OrderOut, dependencies=[Depends(require_permissions("orders.manage"))])
def close_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.close_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Comanda non trovata")
    return order
