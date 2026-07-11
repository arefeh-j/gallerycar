from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.car import Car
from app.models.user import User
from app.models.brand import Brand
from app.models.order import Order

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/api/dashboard")
def dashboard_stats(db: Session = Depends(get_db)):

    return {
        "cars": db.query(Car).count(),
        "users": db.query(User).count(),
        "brands": db.query(Brand).count(),
        "orders": db.query(Order).count()
    }