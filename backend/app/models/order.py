from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    car_id = Column(Integer, ForeignKey("cars.id"))

    status = Column(String, default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    car = relationship("Car")