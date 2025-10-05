from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.core.db import get_db
from backend.modules.tables import crud, schemas
from backend.modules.areas.crud import get_area

router = APIRouter(prefix="/tables", tags=["Tables"])

@router.get("/", response_model=List[schemas.TableOut])
def list_tables(db: Session = Depends(get_db)):
    return crud.list_tables(db)

@router.get("/by-area/{area_id}", response_model=List[schemas.TableOut])
def list_by_area(area_id: int, db: Session = Depends(get_db)):
    if not get_area(db, area_id):
        raise HTTPException(status_code=404, detail="Area not found")
    return crud.list_tables_by_area(db, area_id)

@router.post("/", response_model=schemas.TableOut, status_code=status.HTTP_201_CREATED)
def create_table(payload: schemas.TableCreate, db: Session = Depends(get_db)):
    # area deve esistere
    if not get_area(db, payload.area_id):
        raise HTTPException(status_code=404, detail="Area not found")
    # opzionale: nome tavolo unico dentro la stessa area
    exists = crud.get_table_by_name_in_area(db, payload.area_id, payload.name)
    if exists:
        raise HTTPException(status_code=409, detail="Table name already exists in this area")
    return crud.create_table(db, payload)

@router.get("/{table_id}", response_model=schemas.TableOut)
def get_table(table_id: int, db: Session = Depends(get_db)):
    table = crud.get_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

@router.put("/{table_id}", response_model=schemas.TableOut)
def update_table(table_id: int, payload: schemas.TableUpdate, db: Session = Depends(get_db)):
    table = crud.get_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    # opzionale: se cambia nome, verifica unicità in area
    if payload.name and payload.name != table.name:
        exists = crud.get_table_by_name_in_area(db, table.area_id, payload.name)
        if exists:
            raise HTTPException(status_code=409, detail="Table name already exists in this area")
    return crud.update_table(db, table, payload)

@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = crud.get_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    crud.delete_table(db, table)
