from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from sqlalchemy import ForeignKey, DateTime
from datetime import datetime

from app.database import get_db

from app.models.order import Order
from app.models.car import Car
from app.models.user import User

from app.core.security import get_current_user

router = APIRouter()


class OrderCreate(BaseModel):
    car_id: int


@router.post("/api")
async def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    car = db.query(Car).filter(Car.id == data.car_id).first()

    if not car:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    new_order = Order(
        user_id=current_user.id,
        car_id=data.car_id,
        status="pending"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "message": "سفارش ثبت شد",
        "id": new_order.id
    }
@router.get("/api/admin")
async def get_all_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    orders = db.query(Order).all()

    return [
        {
            "id": order.id,
            "user": order.user.full_name,
            "phone": order.user.phone,
            "car": f"{order.car.brand.name} {order.car.model}",
            "status": order.status,
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for order in orders
    ]


from pydantic import BaseModel

class OrderUpdate(BaseModel):
    status: str


@router.put("/api/{order_id}")
async def update_order_status(
    order_id: int,
    data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = data.status

    db.commit()

    return {"message": "updated"}



@router.delete("/api/{order_id}")
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)

    db.commit()

    return {"message": "deleted"}




    


