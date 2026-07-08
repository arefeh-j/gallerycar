from fastapi import FastAPI, Request
from app.routes.favorites import router as favorites_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes.cars import router as cars_router
from app.routes.users import router as users_router
from app.database import engine, Base

from app.models import user
from app.models import brand
from app.models import car
from app.models import favorite
from app.models import car_image
from app.models import price_history

from app.routes.brands import router as brands_router

import json
import os

CARS_FILE = "cars.json"
USERS_FILE = "users.json"


def load_cars():
    if not os.path.exists(CARS_FILE):
        return []

    with open(CARS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Car Gallery")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(cars_router, prefix="/cars")
app.include_router(users_router, prefix="/users")
app.include_router(favorites_router, prefix="/favorites")
app.include_router(brands_router, prefix="/brands")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def root(request: Request):

    cars = load_cars()
    users = load_users()

    total_cars = len(cars)
    total_users = len(users)

    available_cars = sum(
        1 for car in cars
        if car.get("status") == "available"
    )

    sold_cars = sum(
        1 for car in cars
        if car.get("status") == "sold"
    )

    brands = len(set(car.get("brand", "") for car in cars if car.get("brand")))

    if cars:
       cheapest = min(cars, key=lambda x: x.get("price", float("inf")))
       expensive = max(cars, key=lambda x: x.get("price", float("-inf")))
    else:
       cheapest = None
       expensive = None

    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={
            "total_cars": total_cars,
            "total_users": total_users,
            "available_cars": available_cars,
            "sold_cars": sold_cars,
            "brands": brands,
            "cheapest": cheapest,
            "expensive": expensive,
        }
    )