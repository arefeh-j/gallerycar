from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.favorite import Favorite
from app.models.car import Car
from app.core.security import get_current_user

from fastapi import HTTPException

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

# ==========================
# REST API - Get Favorites
# ==========================

@router.get("/api")
async def get_favorites(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).all()

    return [
        {
            "id": favorite.id,
            "car": {
                "id": favorite.car.id,
                "model": favorite.car.model,
                "price": float(favorite.car.price),
                "year": favorite.car.year
            }
        }
        for favorite in favorites
    ]


# ==========================
# REST API - Add Favorite
# ==========================

@router.post("/api/{car_id}")
async def add_favorite_api(
    car_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    car = db.query(Car).filter(
        Car.id == car_id
    ).first()

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    exists = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.car_id == car_id
    ).first()

    if exists:
    raise HTTPException(
        status_code=400,
        detail="Car already in favorites"
    )

    favorite = Favorite(
        user_id=current_user.id,
        car_id=car_id
    )

    db.add(favorite)
    db.commit()

    return {
        "message": "Added successfully"
    }


# ==========================
# REST API - Delete Favorite
# ==========================

@router.delete("/api/{favorite_id}")
async def delete_favorite_api(
    favorite_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    favorite = db.query(Favorite).filter(
        Favorite.id == favorite_id,
        Favorite.user_id == current_user.id
    ).first()

    if favorite is None:
        raise HTTPException(
            status_code=404,
            detail="Favorite not found"
        )

    db.delete(favorite)
    db.commit()

    return {
        "message": "Deleted successfully"
    }
# ==========================
# REST API - Favorite Status
# ==========================

@router.get("/api/status/{car_id}")
async def favorite_status(
    car_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.car_id == car_id
    ).first()

    return {
        "is_favorite": favorite is not None
    }


@router.post("/api/{car_id}")
async def add_favorite_api(
    car_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    car = db.query(Car).filter(
        Car.id == car_id
    ).first()

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    exists = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.car_id == car_id
    ).first()

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Car already in favorites"
        )

    favorite = Favorite(
        user_id=current_user.id,
        car_id=car_id
    )

    db.add(favorite)
    db.commit()

    return {
        "message": "Added successfully"
    }