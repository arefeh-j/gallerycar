from pydantic import BaseModel
from decimal import Decimal



class PriceHistoryBase(BaseModel):

    old_price: Decimal
    new_price: Decimal



class PriceHistoryCreate(PriceHistoryBase):

    car_id: int



class PriceHistoryResponse(PriceHistoryBase):

    id: int
    car_id: int


    class Config:
        from_attributes = True