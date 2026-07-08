from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.car import Car
from app.schemas.car import CarCreate, CarResponse



router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)



@router.get("/", response_model=list[CarResponse])
def get_cars(
    db: Session = Depends(get_db)
):

    cars = db.query(Car).all()

    return cars




@router.post("/", response_model=CarResponse)
def create_car(
    car: CarCreate,
    db: Session = Depends(get_db)
):

    new_car = Car(

        user_id=car.user_id,
        brand_id=car.brand_id,
        model=car.model,
        year=car.year,
        price=car.price,
        mileage=car.mileage,
        color=car.color,
        fuel_type=car.fuel_type,
        transmission=car.transmission,
        description=car.description

    )


    db.add(new_car)
    db.commit()
    db.refresh(new_car)


    return new_car