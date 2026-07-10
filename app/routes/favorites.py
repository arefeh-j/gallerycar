from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.favorite import Favorite
from app.models.car import Car
from app.core.security import get_current_user

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


# ==========================
# Favorites Landing
# ==========================

@router.get("/landing", response_class=HTMLResponse)
async def favorites_landing(
    request: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="favorites/favorites_landing.html",
        context={
            "request": request,
            "favorites": favorites
        }
    )

# ==========================
# Add Favorite
# ==========================

@router.get("/add/{car_id}")
async def add_to_favorites(
    car_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    car = db.query(Car).filter(Car.id == car_id).first()

    if car is None:
        return RedirectResponse(
            "/cars/landing",
            status_code=303
        )

    exists = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.car_id == car_id
    ).first()
    if exists is None:

        favorite = Favorite(
            user_id=current_user.id,
            car_id=car_id
        )

        db.add(favorite)
        db.commit()

    return RedirectResponse(
        "/favorites/landing",
        status_code=303
    )


# ==========================
# Delete Favorite
# ==========================

@router.get("/delete/{favorite_id}")
async def delete_favorite(
    favorite_id: int,
    db: Session = Depends(get_db)
):

    favorite = db.query(Favorite).filter(
        Favorite.id == favorite_id
    ).first()

    if favorite:

        print(f"Deleting favorite id={favorite_id}")

        db.delete(favorite)
        db.commit()

    return RedirectResponse(
        "/favorites/landing",
        status_code=303
    )
