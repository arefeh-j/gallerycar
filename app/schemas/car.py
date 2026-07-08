from pydantic import BaseModel
from typing import Optional


class CarBase(BaseModel):

    brand_id: int
    model: str
    year: int
    price: float
    mileage: int
    color: Optional[str] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    description: Optional[str] = None
    status: str


class CarCreate(CarBase):
    user_id: int


class CarUpdate(CarBase):
    pass


class CarResponse(CarBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True