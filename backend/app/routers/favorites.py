from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate, FavoriteResponse



router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)



@router.get("/{user_id}", response_model=list[FavoriteResponse])
def get_favorites(
    user_id:int,
    db:Session = Depends(get_db)
):

    favorites = (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id)
        .all()
    )


    return favorites




@router.post("/", response_model=FavoriteResponse)
def add_favorite(
    favorite:FavoriteCreate,
    db:Session = Depends(get_db)
):

    new_favorite = Favorite(

        user_id=favorite.user_id,
        car_id=favorite.car_id

    )


    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)


    return new_favorite