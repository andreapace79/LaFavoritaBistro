from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.modules.areas.models import Area
from backend.modules.areas.schemas import AreaCreate, AreaUpdate

def list_areas(db: Session):
    return db.execute(select(Area)).scalars().all()

def get_area(db: Session, area_id: int):
    return db.get(Area, area_id)

def get_area_by_name(db: Session, name: str):
    stmt = select(Area).where(Area.name == name)
    return db.execute(stmt).scalar_one_or_none()

def create_area(db: Session, data: AreaCreate):
    area = Area(name=data.name, layout_meta=data.layout_meta)
    db.add(area)
    db.commit()
    db.refresh(area)
    return area

def update_area(db: Session, area: Area, data: AreaUpdate):
    if data.name is not None:
        area.name = data.name
    if data.layout_meta is not None:
        area.layout_meta = data.layout_meta
    db.commit()
    db.refresh(area)
    return area

def delete_area(db: Session, area: Area):
    db.delete(area)
    db.commit()
