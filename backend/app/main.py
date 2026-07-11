from fastapi import FastAPI

from app.database.database import engine, Base

from app.models import *
from fastapi import FastAPI

from app.database.database import engine, Base

from app.models import *

from app.routers import users
from app.routers import brands
from app.routers import cars
from app.routers import favorites
from app.routers import orders
from app.routers import admin




app = FastAPI(
    title="Car Gallery API",
    version="0.1.0"
)



Base.metadata.create_all(
    bind=engine
)

app.include_router(admin.router)

app.include_router(
    users.router
)

app.include_router(
    brands.router
)

app.include_router(
    cars.router
)

app.include_router(
    favorites.router
)

app.include_router(
    orders.router,
    prefix="/orders",
    tags=["Orders"]
)


@app.get("/")
def home():

    return {
        "message":"Car Gallery API is running"
    }




app = FastAPI(
    title="Car Gallery API",
    version="0.1.0"
)



Base.metadata.create_all(
    bind=engine
)

app.include_router(admin.router)

app.include_router(
    users.router
)

app.include_router(
    brands.router
)

app.include_router(
    cars.router
)

app.include_router(
    favorites.router
)

app.include_router(
    orders.router,
    prefix="/orders",
    tags=["Orders"]
)


@app.get("/")
def home():

    return {
        "message":"Car Gallery API is running"
    }