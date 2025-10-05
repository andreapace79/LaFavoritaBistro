from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.core.db import get_db
from backend.modules.areas import crud, schemas

router = APIRouter(prefix="/areas", tags=["Areas"])

@router.get("/", response_model=List[schemas.AreaOut])
def list_areas(db: Session = Depends(get_db)):
    return crud.list_areas(db)

@router.post("/", response_model=schemas.AreaOut, status_code=status.HTTP_201_CREATED)
def create_area(payload: schemas.AreaCreate, db: Session = Depends(get_db)):
    exists = crud.get_area_by_name(db, payload.name)
    if exists:
        raise HTTPException(status_code=409, detail="Area name already exists")
    return crud.create_area(db, payload)

@router.get("/{area_id}", response_model=schemas.AreaOut)
def get_area(area_id: int, db: Session = Depends(get_db)):
    area = crud.get_area(db, area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    return area

@router.put("/{area_id}", response_model=schemas.AreaOut)
def update_area(area_id: int, payload: schemas.AreaUpdate, db: Session = Depends(get_db)):
    area = crud.get_area(db, area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    # opzionale: controllo nome duplicato se cambiato
    if payload.name and payload.name != area.name:
        exists = crud.get_area_by_name(db, payload.name)
        if exists:
            raise HTTPException(status_code=409, detail="Area name already exists")
    return crud.update_area(db, area, payload)

@router.delete("/{area_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_area(area_id: int, db: Session = Depends(get_db)):
    area = crud.get_area(db, area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    crud.delete_area(db, area)
