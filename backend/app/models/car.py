from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL, Enum, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Car(Base):

    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)

    model = Column(String(100), nullable=False)

    year = Column(Integer, nullable=False)

    price = Column(DECIMAL(12,2), nullable=False)

    mileage = Column(Integer, default=0)

    color = Column(String(50))

    fuel_type = Column(String(50))

    transmission = Column(String(50))

    description = Column(Text)

    status = Column(
        Enum("pending","approved","rejected"),
        default="pending"
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    owner = relationship(
        "User",
        back_populates="cars"
    )

    brand = relationship(
        "Brand",
        back_populates="cars"
    )

    favorites = relationship(
        "Favorite",
        back_populates="car"
    )

    images = relationship(
        "CarImage",
        back_populates="car"
    )

    price_history = relationship(
        "PriceHistory",
        back_populates="car"
    )