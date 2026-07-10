from fastapi import APIRouter, Request, Query, Depends, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import or_
import math

from app.schemas.user import UserUpdate
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.database import get_db
from app.models.user import User
from app.core.security import get_current_user
from pydantic import BaseModel


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

ITEMS_PER_PAGE = 5
@router.get("/landing", response_class=HTMLResponse)
async def users_landing(
    request: Request,
    db: Session = Depends(get_db),
    sort: str = Query("default"),
    page: int = Query(1, ge=1),
    search: str = Query("")
):

    query = db.query(User)

    if search:

        query = query.filter(
            or_(
                User.full_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.phone.ilike(f"%{search}%")
            )
        )

    if sort == "name":

        query = query.order_by(User.full_name)

    elif sort == "email":

        query = query.order_by(User.email)

    else:

        query = query.order_by(User.id)

    total_items = query.count()

    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)

    users = query.offset(
        (page - 1) * ITEMS_PER_PAGE
    ).limit(
        ITEMS_PER_PAGE
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="users/users_landing.html",
        context={
            "users": users,
            "total_items": total_items,
            "current_page": page,
            "total_pages": total_pages,
            "sort": sort,
            "search": search
        }
    )
# ==========================
# Add User
# ==========================

@router.get("/add", response_class=HTMLResponse)
async def add_user_form(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="users/user_form.html",
        context={
            "editing": False,
            "user": None
        }
    )


@router.post("/")
async def create_user(

    request: Request,

    db: Session = Depends(get_db),

    name: str = Form(...),

    email: str = Form(...),

    phone: str = Form(...),

    password: str = Form(...)

):

    old_user = db.query(User).filter(User.email == email).first()

    if old_user:

        return templates.TemplateResponse(
            request=request,
            name="users/user_form.html",
            context={
                "editing": False,
                "user": None,
                "error": "This email already exists."
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    new_user = User(
        full_name=name,
        email=email,
        phone=phone,
        password=hash_password(password),
        role="user"
    )

    db.add(new_user)

    db.commit()

    return RedirectResponse(
        "/users/landing",
        status_code=status.HTTP_303_SEE_OTHER
    )


# ==========================
# Edit User
# ==========================

@router.get("/edit/{user_id}", response_class=HTMLResponse)
async def edit_user_form(

    request: Request,

    user_id: int,

    db: Session = Depends(get_db)

):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="users/user_form.html",
        context={
            "editing": True,
            "user": user
        }
    )


@router.post("/{user_id}")
async def update_user(

    user_id: int,

    db: Session = Depends(get_db),

    name: str = Form(...),

    email: str = Form(...),

    phone: str = Form(...),

    password: str = Form(...)

):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.full_name = name
    user.email = email
    user.phone = phone
    user.password = hash_password(password)

    db.commit()

    return RedirectResponse(
        "/users/landing",
        status_code=status.HTTP_303_SEE_OTHER
    )
# ==========================
# Show Delete Page
# ==========================

@router.get("/delete/{user_id}", response_class=HTMLResponse)
async def confirm_delete(

    request: Request,

    user_id: int,

    db: Session = Depends(get_db)

):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="users/user_delete.html",
        context={
            "user": user
        }
    )


# ==========================
# Delete User
# ==========================

@router.post("/delete/{user_id}")
async def delete_user(

    user_id: int,

    db: Session = Depends(get_db)

):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)

    db.commit()

    return RedirectResponse(
        "/users/landing",
        status_code=status.HTTP_303_SEE_OTHER
    )
class RegisterRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/api/register")
async def register_api(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    old_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if old_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user = User(
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        password=hash_password(data.password),
        role="user"
    )

    db.add(user)

    db.commit()

    return {
        "message": "User registered successfully"
    }
@router.post("/api/login")
async def login_api(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="ایمیل یا رمز عبور اشتباه است."
        )

    if not verify_password(
        data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="ایمیل یا رمز عبور اشتباه است."
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "full_name": user.full_name,
        "role": user.role
    }

# ==========================
# Current User API
# ==========================

@router.get("/api/me")
async def current_user(
    current_user = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone": current_user.phone,
        "role": current_user.role
    }



# ==========================
# Current User API
# ==========================

from app.core.security import get_current_user


@router.put("/api/me")
async def update_profile(
    data: UserUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if data.full_name:
        current_user.full_name = data.full_name

    if data.email:
        current_user.email = data.email

    if data.phone:
        current_user.phone = data.phone

    if data.password:
        current_user.password = hash_password(data.password)

    db.commit()
    db.refresh(current_user)

    return {
        "message": "پروفایل با موفقیت بروزرسانی شد.",
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "phone": current_user.phone
        }
    }