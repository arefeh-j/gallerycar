from pydantic import BaseModel



class FavoriteBase(BaseModel):

    car_id: int



class FavoriteCreate(FavoriteBase):

    user_id: int



class FavoriteResponse(FavoriteBase):

    id: int
    user_id: int


    class Config:
        from_attributes = True