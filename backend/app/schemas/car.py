from pydantic import BaseModel
from typing import Optional
from decimal import Decimal



class CarBase(BaseModel):

    brand_id: int
    model: str
    year: int
    price: Decimal
    mileage: Optional[int] = 0
    color: Optional[str] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    description: Optional[str] = None



class CarCreate(CarBase):

    user_id: int



class CarUpdate(BaseModel):

    price: Optional[Decimal] = None
    color: Optional[str] = None
    mileage: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None



class CarResponse(CarBase):

    id: int
    user_id: int
    status: str


    class Config:
        from_attributes = True