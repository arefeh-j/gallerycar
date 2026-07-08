from sqlalchemy import Column,Integer,DECIMAL,ForeignKey
from app.database.database import Base


class PriceHistory(Base):

    __tablename__="price_history"


    id=Column(
        Integer,
        primary_key=True
    )


    car_id=Column(
        Integer,
        ForeignKey("cars.id")
    )


    old_price=Column(
        DECIMAL(12,2)
    )


    new_price=Column(
        DECIMAL(12,2)
    )