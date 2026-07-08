from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):

    full_name: str
    email: str
    phone: Optional[str] = None
    role: Optional[str] = "user"



class UserCreate(UserBase):

    password: str



class UserUpdate(BaseModel):

    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None



class UserResponse(UserBase):

    id: int


    class Config:
        from_attributes = True