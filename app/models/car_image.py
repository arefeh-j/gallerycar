from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class CarImage(Base):

    __tablename__ = "car_images"

    id = Column(Integer, primary_key=True, index=True)

    car_id = Column(
        Integer,
        ForeignKey("cars.id", ondelete="CASCADE"),
        nullable=False
    )

    image_url = Column(
        String(255),
        nullable=False
    )

    is_main = Column(
        Boolean,
        default=False
    )

    car = relationship(
        "Car",
        back_populates="images"
    )