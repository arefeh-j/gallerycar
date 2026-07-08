from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, Enum, ForeignKey, TIMESTAMP
from app.database.database import Base


class Car(Base):

    __tablename__ = "cars"


    id = Column(
        Integer,
        primary_key=True
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )


    brand_id = Column(
        Integer,
        ForeignKey("brands.id")
    )


    model = Column(
        String(100)
    )


    year = Column(
        Integer
    )


    price = Column(
        DECIMAL(12,2)
    )


    mileage = Column(
        Integer
    )


    color = Column(
        String(50)
    )


    fuel_type = Column(
        String(50)
    )


    transmission = Column(
        String(50)
    )


    country = Column(
        String(50)
    )


    engine_volume = Column(
        String(20)
    )


    description = Column(
        Text
    )


    status = Column(
        Enum(
            "pending",
            "approved",
            "rejected",
            "sold"
        ),
        default="pending"
    )


    is_sold = Column(
        Boolean,
        default=False
    )