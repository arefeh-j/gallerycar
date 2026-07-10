from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.car import Car
from app.schemas.car import CarCreate, CarResponse


router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)


# دریافت همه خودروها
@router.get("/", response_model=list[CarResponse])
def get_cars(
    db: Session = Depends(get_db)
):
    cars = db.query(Car).all()
    return cars


# دریافت یک خودرو بر اساس شناسه
@router.get("/{car_id}", response_model=CarResponse)
def get_car(
    car_id: int,
    db: Session = Depends(get_db)
):

    car = db.query(Car).filter(Car.id == car_id).first()

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return car


# ثبت خودرو
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