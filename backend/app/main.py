from fastapi import FastAPI

from app.database.database import engine, Base

from app.models import *

from app.routers import users
from app.routers import brands
from app.routers import cars
from app.routers import favorites



app = FastAPI(
    title="Car Gallery API",
    version="0.1.0"
)



Base.metadata.create_all(
    bind=engine
)



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



@app.get("/")
def home():

    return {
        "message":"Car Gallery API is running"
    }