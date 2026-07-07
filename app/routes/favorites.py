from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import json
import os

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

FAVORITES_FILE = "favorites.json"
CARS_FILE = "cars.json"


def load_favorites():
    if not os.path.exists(FAVORITES_FILE):
        return []

    with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_favorites(favorites):
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump(favorites, f, indent=4)


def load_cars():
    if not os.path.exists(CARS_FILE):
        return []

    with open(CARS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/landing", response_class=HTMLResponse)
async def favorites_landing(request: Request):

    favorites = load_favorites()

    return templates.TemplateResponse(
        request=request,
        name="favorites/favorites_landing.html",
        context={
            "favorites": favorites
        }
    )


@router.get("/add/{car_id}")
async def add_to_favorites(car_id: str):

    favorites = load_favorites()
    cars = load_cars()

    for car in cars:

        if car["id"] == car_id:

            exists = False

            for fav in favorites:

                if fav["id"] == car_id:
                    exists = True
                    break

            if not exists:
                favorites.append(car)
                save_favorites(favorites)

            break

    return RedirectResponse(
        "/favorites/landing",
        status_code=303
    )


@router.get("/delete/{car_id}")
async def delete_favorite(car_id: str):

    favorites = load_favorites()

    new_favorites = []

    for car in favorites:

        if car["id"] != car_id:
            new_favorites.append(car)

    save_favorites(new_favorites)

    return RedirectResponse(
        "/favorites/landing",
        status_code=303
    )