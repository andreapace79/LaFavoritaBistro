from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum

class TableStatus(str, Enum):
    free = "free"
    occupied = "occupied"
    reserved = "reserved"
    disabled = "disabled"

class TableBase(BaseModel):
    area_id: int
    name: str = Field(min_length=1, max_length=100)
    seats: int = Field(ge=0, default=0)
    status: TableStatus = TableStatus.free

class TableCreate(TableBase):
    pass

class TableUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    seats: Optional[int] = Field(default=None, ge=0)
    status: Optional[TableStatus] = None

class TableOut(TableBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
