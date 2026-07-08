from pydantic import BaseModel
from typing import Optional



class CarImageBase(BaseModel):

    image_url: str
    is_main: Optional[bool] = False



class CarImageCreate(CarImageBase):

    car_id: int



class CarImageResponse(CarImageBase):

    id: int
    car_id: int


    class Config:
        from_attributes = True