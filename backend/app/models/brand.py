from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Brand(Base):

    __tablename__ = "brands"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(100),
        nullable=False
    )


    country = Column(
        String(50)
    )