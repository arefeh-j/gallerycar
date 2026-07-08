from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class PriceHistory(Base):

    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)

    car_id = Column(
        Integer,
        ForeignKey("cars.id", ondelete="CASCADE"),
        nullable=False
    )

    old_price = Column(DECIMAL(12,2))

    new_price = Column(DECIMAL(12,2))

    changed_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    car = relationship(
        "Car",
        back_populates="price_history"
    )