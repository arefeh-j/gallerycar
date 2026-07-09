
from fastapi import APIRouter, Request, Query, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Form, status, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from sqlalchemy import or_

import math

from app.database import get_db
from app.models.car import Car
from app.models.brand import Brand
from app.models.user import User

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

ITEMS_PER_PAGE = 5
@router.get("/landing", response_class=HTMLResponse)
async def cars_landing(

    request: Request,

    db: Session = Depends(get_db),

    sort: str = Query("default"),

    page: int = Query(1, ge=1),

    search: str = Query("")

):
    print("✅ CARS ROUTE WORKING")
    query = db.query(Car)

    if search:

        query = query.filter(

            or_(

                Car.model.ilike(f"%{search}%")

            )

        )

    if sort == "price":

        query = query.order_by(Car.price)

    elif sort == "year":

        query = query.order_by(Car.year)

    elif sort == "mileage":

        query = query.order_by(Car.mileage)

    else:

        query = query.order_by(Car.id)

    total_items = query.count()

    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)

    cars = query.offset(

        (page - 1) * ITEMS_PER_PAGE

    ).limit(

        ITEMS_PER_PAGE

    ).all()

    return templates.TemplateResponse(

        request=request,

        name="cars/cars_landing.html",

        context={

            "cars": cars,

            "total_items": total_items,

            "current_page": page,

            "total_pages": total_pages,

            "sort": sort,

            "search": search

        }

    )

@router.get("/add", response_class=HTMLResponse)
async def add_car_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="cars/car_form.html",
        context={
            "editing": False,
            "car": None,
            "car_id": None
        }
    )
@router.post("/")
async def create_car(

    request: Request,

    db: Session = Depends(get_db),

    brand_id: int = Form(...),

    user_id: int = Form(...),

    model: str = Form(...),

    year: int = Form(...),

    price: float = Form(...),

    mileage: int = Form(...),

    color: str = Form(...),

    fuel_type: str = Form(...),

    transmission: str = Form(...),

    description: str = Form(...)

):
    print("CREATE CAR CALLED")


    new_car = Car(

        user_id=user_id,

        brand_id=brand_id,

        model=model,

        year=year,

        price=price,

        mileage=mileage,

        color=color,

        fuel_type=fuel_type,

        transmission=transmission,

        description=description

    )

    db.add(new_car)

    db.commit()

    return RedirectResponse(

        "/cars/landing",

        status_code=status.HTTP_303_SEE_OTHER

    )

@router.get("/edit/{car_id}", response_class=HTMLResponse)
async def edit_car_form(

    request: Request,

    car_id: int,

    db: Session = Depends(get_db)

):

    car = db.query(Car).filter(Car.id == car_id).first()

    if car is None:

        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="cars/car_form.html",
        context={
            "editing": True,
            "car": car
        }
    )

@router.get("/view/{car_id}", response_class=HTMLResponse)
async def view_car(

    request: Request,

    car_id: int,

    db: Session = Depends(get_db)

):

    car = db.query(Car).filter(Car.id == car_id).first()

    if car is None:

        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="cars/car_view.html",
        context={
            "request": request,
            "car": car
        }
    )

@router.post("/{car_id}")
async def update_car(

    car_id: int,

    db: Session = Depends(get_db),

    user_id: int = Form(...),

    brand_id: int = Form(...),

    model: str = Form(...),

    year: int = Form(...),

    price: float = Form(...),

    mileage: int = Form(...),

    color: str = Form(...),

    fuel_type: str = Form(...),

    transmission: str = Form(...),

    description: str = Form(...)

):

    car = db.query(Car).filter(Car.id == car_id).first()

    if car is None:

        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    car.user_id = user_id
    car.brand_id = brand_id
    car.model = model
    car.year = year
    car.price = price
    car.mileage = mileage
    car.color = color
    car.fuel_type = fuel_type
    car.transmission = transmission
    car.description = description

    db.commit()

    return RedirectResponse(
        "/cars/landing",
        status_code=status.HTTP_303_SEE_OTHER
    )
# ==========================
# Show Delete Confirmation
# ==========================
@router.get("/delete/{car_id}", response_class=HTMLResponse)
async def confirm_delete(

    request: Request,

    car_id: int,

    db: Session = Depends(get_db)

):

    car = db.query(Car).filter(Car.id == car_id).first()

    if car is None:

        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="cars/car_delete.html",
        context={
            "car": car
        }
    )


# ==========================
# Delete Car
# ==========================
@router.post("/delete/{car_id}")
async def delete_car(

    car_id: int,

    db: Session = Depends(get_db)

):

    car = db.query(Car).filter(Car.id == car_id).first()

    if car is None:

        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    db.delete(car)
    print("Images:", len(car.images))
    print("Favorites:", len(car.favorites))
    print("History:", len(car.price_history))

    db.commit()

    return RedirectResponse(
        "/cars/landing",
        status_code=status.HTTP_303_SEE_OTHER
    )
# ==========================
# REST API - Cars
# ==========================

@router.get("")
async def get_cars_api(
    db: Session = Depends(get_db)
):

    cars = db.query(Car).all()

    result = []

    for car in cars:
        result.append({
            "id": car.id,
            "model": car.model,
            "year": car.year,
            "price": float(car.price),
            "brand": car.brand.name if car.brand else "",
            "owner": car.owner.full_name if car.owner else ""
        })

    return result
# ==========================
# REST API - Cars
# ==========================

@router.get("/api")
async def get_cars_api(
    db: Session = Depends(get_db)
):

    cars = db.query(Car).all()

    return [
        {
            "id": car.id,
            "model": car.model,
            "year": car.year,
            "price": float(car.price),
            "brand": car.brand.name if car.brand else ""
        }
        for car in cars
    ]