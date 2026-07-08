from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users



@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=user.password,
        phone=user.phone,
        role=user.role
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user