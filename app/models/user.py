from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    phone = Column(String(20))

    role = Column(
        Enum("admin", "user"),
        default="user"
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    cars = relationship(
        "Car",
        back_populates="owner"
    )

    favorites = relationship(
        "Favorite",
        back_populates="user"
    )