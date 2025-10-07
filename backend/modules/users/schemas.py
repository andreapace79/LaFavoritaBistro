from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str   # plain in input

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

