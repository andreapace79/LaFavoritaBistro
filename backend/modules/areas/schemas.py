from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any

class AreaBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    layout_meta: Optional[Any] = None  # JSON arbitrario

class AreaCreate(AreaBase):
    pass

class AreaUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    layout_meta: Optional[Any] = None

class AreaOut(AreaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
