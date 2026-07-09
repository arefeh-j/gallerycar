from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import engine, Base, get_db

from app.routes.cars import router as cars_router
from app.routes.users import router as users_router
from app.routes.favorites import router as favorites_router
from app.routes.brands import router as brands_router

from app.models import user
from app.models import brand
from app.models import car
from app.models import favorite
from app.models import car_image
from app.models import price_history

from app.models.user import User
from app.models.car import Car
from app.models.brand import Brand

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Car Gallery")

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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