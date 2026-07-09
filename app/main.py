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

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.user import User
from app.models.car import Car
from app.models.brand import Brand

from fastapi import Depends



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Car Gallery")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(cars_router, prefix="/cars")
app.include_router(users_router, prefix="/users")
app.include_router(favorites_router, prefix="/favorites")
app.include_router(brands_router, prefix="/brands")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def root(
    request: Request,
    db: Session = Depends(get_db)
):

    cars = db.query(Car).all()
    users = db.query(User).all()

    total_cars = len(cars)
    total_users = len(users)

    available_cars = db.query(Car).filter(
        Car.status == "approved"
    ).count()

    sold_cars = 0

    brands = db.query(Brand).count()

    if cars:
        cheapest = min(cars, key=lambda x: x.price)
        expensive = max(cars, key=lambda x: x.price)
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