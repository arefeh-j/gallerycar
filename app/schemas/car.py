from pydantic import BaseModel
from decimal import Decimal


class CarBase(BaseModel):
    brand_id: int
    user_id: int
    model: str
    year: int
    price: Decimal
    mileage: int
    color: str | None = None
    fuel_type: str | None = None
    transmission: str | None = None
    description: str | None = None
    status: str


class CarCreate(CarBase):
    pass


class CarRead(CarBase):
    id: int

    class Config:
        from_attributes = True