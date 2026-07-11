from fastapi import APIRouter, Request, Query, Depends, Form, status, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_
import math
from pydantic import BaseModel
from typing import List, Optional

from app.database import get_db
from app.models.car import Car
from app.models.brand import Brand
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
ITEMS_PER_PAGE = 5

# ==========================
# Pydantic Schemas for API
# ==========================
class CarCreate(BaseModel):
    brand_id: int
    model: str
    year: int
    price: float
    mileage: Optional[int] = 0
    color: Optional[str] = ""
    fuel_type: Optional[str] = ""
    transmission: Optional[str] = ""
    description: Optional[str] = ""

class CarUpdate(BaseModel):
    brand_id: int
    model: str
    year: int
    price: float
    mileage: Optional[int] = 0
    color: Optional[str] = ""
    fuel_type: Optional[str] = ""
    transmission: Optional[str] = ""
    description: Optional[str] = ""

# ======================================================
# REST API (JSON) – باید اول باشند
# ======================================================

@router.get("/api")
async def get_cars_api(db: Session = Depends(get_db)):
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

@router.post("/api")
async def create_car_api(
    data: CarCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_car = Car(
        user_id=current_user.id,
        brand_id=data.brand_id,
        model=data.model,
        year=data.year,
        price=data.price,
        mileage=data.mileage or 0,
        color=data.color or "",
        fuel_type=data.fuel_type or "",
        transmission=data.transmission or "",
        description=data.description or "",
        status="approved"
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return {"id": new_car.id, "message": "خودرو با موفقیت ثبت شد"}

# ===== اضافه شده: آگهی‌های من (فقط خودروهای این کاربر) =====
@router.get("/api/my")
async def get_my_cars(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cars = db.query(Car).filter(Car.user_id == current_user.id).all()
    return [
        {
            "id": car.id,
            "brand": car.brand.name if car.brand else "",
            "model": car.model,
            "price": float(car.price),
            "status": car.status,
            "image": car.images[0].image_url if car.images else None
        }
        for car in cars
    ]

@router.get("/api/admin")
async def admin_cars(db: Session = Depends(get_db)):
    cars = db.query(Car).all()
    return [
        {
            "id": car.id,
            "brand": car.brand.name if car.brand else "",
            "model": car.model,
            "price": float(car.price),
            "status": car.status
        }
        for car in cars
    ]

@router.post("/api/admin/{car_id}/approve")
async def approve_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    car.status = "approved"
    db.commit()
    return {"message": "approved"}

@router.post("/api/admin/{car_id}/reject")
async def reject_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    car.status = "rejected"
    db.commit()
    return {"message": "rejected"}

@router.delete("/api/admin/{car_id}")
async def delete_car_api(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(car)
    db.commit()
    return {"message": "deleted"}

# ===== آپلود تصاویر =====
@router.post("/api/{car_id}/images")
async def upload_car_images(
    car_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": f"{len(files)} images uploaded"}

# ===== جزئیات خودرو (باید آخرین مسیر API باشد) =====
@router.get("/api/{car_id}")
def get_car_detail(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return {
        "id": car.id,
        "user_id": car.user_id,
        "brand": car.brand.name if car.brand else "",
        "model": car.model,
        "price": float(car.price),
        "color": car.color,
        "transmission": car.transmission,
        "status": car.status,
        "brand_id": car.brand_id,
        "year": car.year,
        "mileage": car.mileage,
        "fuel_type": car.fuel_type,
        "description": car.description,
        "created_at": car.created_at,
        "images": [
            {"id": image.id, "url": image.image_url}
            for image in car.images
        ]
    }
@router.put("/api/{car_id}")
async def update_car_api(
    car_id: int,
    data: CarUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    car = db.query(Car).filter(Car.id == car_id).first()

    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    # فقط صاحب آگهی یا ادمین بتواند ویرایش کند
    if car.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    car.brand_id = data.brand_id
    car.model = data.model
    car.year = data.year
    car.price = data.price
    car.mileage = data.mileage
    car.color = data.color
    car.fuel_type = data.fuel_type
    car.transmission = data.transmission
    car.description = data.description

    db.commit()
    db.refresh(car)

    return {
        "message": "Car updated successfully"
    }

# ======================================================
# HTML Pages (Jinja2) – باید بعد از APIها باشند
# ======================================================

@router.get("/landing", response_class=HTMLResponse)
async def cars_landing(
    request: Request,
    db: Session = Depends(get_db),
    sort: str = Query("default"),
    page: int = Query(1, ge=1),
    search: str = Query("")
):
    query = db.query(Car)
    if search:
        query = query.filter(or_(Car.model.ilike(f"%{search}%")))
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
    cars = query.offset((page - 1) * ITEMS_PER_PAGE).limit(ITEMS_PER_PAGE).all()

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
        context={"editing": False, "car": None, "car_id": None}
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
    return RedirectResponse("/cars/landing", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/edit/{car_id}", response_class=HTMLResponse)
async def edit_car_form(request: Request, car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return templates.TemplateResponse(
        request=request,
        name="cars/car_form.html",
        context={"editing": True, "car": car}
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
        raise HTTPException(status_code=404, detail="Car not found")
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
    return RedirectResponse("/cars/landing", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/view/{car_id}", response_class=HTMLResponse)
async def view_car(request: Request, car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return templates.TemplateResponse(
        request=request,
        name="cars/car_view.html",
        context={"request": request, "car": car}
    )

@router.get("/delete/{car_id}", response_class=HTMLResponse)
async def confirm_delete(request: Request, car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return templates.TemplateResponse(
        request=request,
        name="cars/car_delete.html",
        context={"car": car}
    )

@router.post("/delete/{car_id}")
async def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(car)
    db.commit()
    return RedirectResponse("/cars/landing", status_code=status.HTTP_303_SEE_OTHER)