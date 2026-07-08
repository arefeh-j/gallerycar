from pydantic import BaseModel


class UserBase(BaseModel):
    full_name: str
    email: str
    phone: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True