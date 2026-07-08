from sqlalchemy import Column,Integer,String,ForeignKey
from app.database.database import Base


class CarImage(Base):

    __tablename__="car_images"


    id=Column(
        Integer,
        primary_key=True
    )


    car_id=Column(
        Integer,
        ForeignKey("cars.id")
    )


    image_path=Column(
        String(255)
    )