from pydantic import BaseModel
from typing import List, Optional

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = False
    tax: Optional[float] = 0.0

class ItemResponse(BaseModel):
    item: Item
    message: str

class ItemsResponse(BaseModel):
    items: List[Item]
    length: int
    message: str