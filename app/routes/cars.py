from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import os
import json
import math

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

CARS_FILE = "cars.json"
ITEMS_PER_PAGE = 5


def load_cars():
    if not os.path.exists(CARS_FILE):
        return []

    with open(CARS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/landing", response_class=HTMLResponse)
async def cars_landing(
    request: Request,
    sort: str = Query(
        "default",
        pattern="^(default|brand|price|year|mileage)$"
    ),
    page: int = Query(1, ge=1),
    search: str = Query(None)
):

    cars = load_cars()

    # Search
    if search:
        search_lower = search.lower()

        filtered = []

        for car in cars:

            if (
                search_lower in car["brand"].lower()
                or search_lower in car["model"].lower()
            ):
                filtered.append(car)

        cars = filtered

    # Sorting
    if sort == "brand":
        cars = sorted(cars, key=lambda x: x["brand"].lower())

    elif sort == "price":
        cars = sorted(cars, key=lambda x: x["price"])

    elif sort == "year":
        cars = sorted(cars, key=lambda x: x["year"])

    elif sort == "mileage":
        cars = sorted(cars, key=lambda x: x["mileage"])

    # Pagination

    total_items = len(cars)

    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    paginated_cars = cars[start:end]

    if page > total_pages and total_pages > 0:

        return RedirectResponse(
            url=f"/cars/landing?sort={sort}&page={total_pages}&search={search or ''}",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="cars/cars_landing.html",
        context={
            "cars": paginated_cars,
            "total_items": total_items,
            "current_page": page,
            "total_pages": total_pages,
            "sort": sort,
            "search": search or "",
        }
    )
from fastapi import Form, status

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


@router.post("/", response_class=HTMLResponse)
async def create_car(
    request: Request,
    id: str = Form(...),
    brand: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    price: int = Form(...),
    mileage: int = Form(...),
    status: str = Form(...),
    seller: str = Form(...)
):

    cars = load_cars()

    # جلوگیری از ثبت شناسه تکراری
    for car in cars:
        if car["id"] == id:

            error_msg = f"Car ID '{id}' already exists."

            return templates.TemplateResponse(
                request=request,
                name="cars/car_form.html",
                context={
                    "editing": False,
                    "car": None,
                    "car_id": None,
                    "error": error_msg,
                    "form_data": {
                        "id": id,
                        "brand": brand,
                        "model": model,
                        "year": year,
                        "price": price,
                        "mileage": mileage,
                        "status": status,
                        "seller": seller
                    }
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

    new_car = {
        "id": id,
        "brand": brand,
        "model": model,
        "year": year,
        "price": price,
        "mileage": mileage,
        "status": status,
        "seller": seller
    }

    cars.append(new_car)

    with open(CARS_FILE, "w", encoding="utf-8") as f:
        json.dump(cars, f, indent=4)

    return RedirectResponse(
        "/cars/landing",
        status_code=status.HTTP_303_SEE_OTHER
    )
from fastapi import HTTPException


@router.get("/edit/{car_id}", response_class=HTMLResponse)
async def edit_car_form(request: Request, car_id: str):

    cars = load_cars()

    car = None

    for c in cars:
        if c["id"] == car_id:
            car = c
            break

    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return templates.TemplateResponse(
        request=request,
        name="cars/car_form.html",
        context={
            "editing": True,
            "car": car,
            "car_id": car_id
        }
    )
@router.get("/view/{car_id}", response_class=HTMLResponse)
async def view_car(request: Request, car_id: str):

    cars = load_cars()

    car = None

    for c in cars:
        if c["id"] == car_id:
            car = c
            break

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

    car_id: str,

    brand: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    price: int = Form(...),
    mileage: int = Form(...),
    status: str = Form(...),
    seller: str = Form(...)

):

    cars = load_cars()

    for i, car in enumerate(cars):

        if car["id"] == car_id:

            cars[i] = {

                "id": car_id,
                "brand": brand,
                "model": model,
                "year": year,
                "price": price,
                "mileage": mileage,
                "status": status,
                "seller": seller

            }

            with open(CARS_FILE, "w", encoding="utf-8") as f:
                json.dump(cars, f, indent=4)

            return RedirectResponse(
                "/cars/landing",
                status_code=status.HTTP_303_SEE_OTHER
            )

    raise HTTPException(status_code=404, detail="Car not found")
# ==========================
# Show Delete Confirmation
# ==========================

@router.get("/delete/{car_id}", response_class=HTMLResponse)
async def confirm_delete(request: Request, car_id: str):

    cars = load_cars()

    car = None

    for c in cars:
        if c["id"] == car_id:
            car = c
            break

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
async def delete_car(car_id: str):

    cars = load_cars()

    new_cars = []

    for car in cars:

        if car["id"] != car_id:
            new_cars.append(car)

    if len(new_cars) == len(cars):
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    with open(CARS_FILE, "w", encoding="utf-8") as f:
        json.dump(new_cars, f, indent=4)

    return RedirectResponse(
        "/cars/landing",
        status_code=status.HTTP_303_SEE_OTHER
    )
@router.get("/view/{car_id}", response_class=HTMLResponse)
async def view_car(request: Request, car_id: str):

    cars = load_cars()

    car = None

    for c in cars:
        if c["id"] == car_id:
            car = c
            break

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="cars/car_view.html",
        context={
            "car": car
        }
    )