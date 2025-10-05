from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from backend.modules.tables.models import Table
from backend.modules.tables.schemas import TableCreate, TableUpdate

def list_tables(db: Session):
    return db.execute(select(Table)).scalars().all()

def list_tables_by_area(db: Session, area_id: int):
    stmt = select(Table).where(Table.area_id == area_id)
    return db.execute(stmt).scalars().all()

def get_table(db: Session, table_id: int):
    return db.get(Table, table_id)

def get_table_by_name_in_area(db: Session, area_id: int, name: str):
    stmt = select(Table).where(and_(Table.area_id == area_id, Table.name == name))
    return db.execute(stmt).scalar_one_or_none()

def create_table(db: Session, data: TableCreate):
    table = Table(
        area_id=data.area_id,
        name=data.name,
        seats=data.seats,
        status=data.status,
    )
    db.add(table)
    db.commit()
    db.refresh(table)
    return table

def update_table(db: Session, table: Table, data: TableUpdate):
    if data.name is not None:
        table.name = data.name
    if data.seats is not None:
        table.seats = data.seats
    if data.status is not None:
        table.status = data.status
    db.commit()
    db.refresh(table)
    return table

def delete_table(db: Session, table: Table):
    db.delete(table)
    db.commit()
