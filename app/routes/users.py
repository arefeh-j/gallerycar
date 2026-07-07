from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form, status, HTTPException
import json
import os
import math

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

USERS_FILE = "users.json"
ITEMS_PER_PAGE = 5


def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


def next_user_id(users):

    if not users:
        return "U001"

    max_num = max(int(u["user_id"][1:]) for u in users)

    return f"U{max_num+1:03d}"


@router.get("/landing", response_class=HTMLResponse)
async def users_landing(

    request: Request,

    sort: str = Query(
        "default",
        pattern="^(default|user_id|name|email)$"
    ),

    page: int = Query(1, ge=1),

    search: str = Query(None)

):

    users = load_users()

    if search:

        search_lower = search.lower()

        filtered = []

        for user in users:

            if (
                search_lower in user["user_id"].lower()
                or search_lower in user["name"].lower()
                or search_lower in user["email"].lower()
            ):
                filtered.append(user)

        users = filtered

    if sort == "user_id":
        users = sorted(users, key=lambda x: x["user_id"])

    elif sort == "name":
        users = sorted(users, key=lambda x: x["name"].lower())

    elif sort == "email":
        users = sorted(users, key=lambda x: x["email"].lower())

    total_items = len(users)

    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    paginated_users = users[start:end]

    return templates.TemplateResponse(
        request=request,
        name="users/users_landing.html",
        context={
            "users": paginated_users,
            "total_items": total_items,
            "current_page": page,
            "total_pages": total_pages,
            "sort": sort,
            "search": search or "",
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
            "user": None,
            "user_id": None
        }
    )


@router.post("/", response_class=HTMLResponse)
async def create_user(

    request: Request,

    name: str = Form(...),

    email: str = Form(...),

    phone: str = Form(...),

    password: str = Form(...)

):

    users = load_users()

    # جلوگیری از ثبت ایمیل تکراری
    for user in users:

        if user["email"] == email:

            return templates.TemplateResponse(
                request=request,
                name="users/user_form.html",
                context={
                    "editing": False,
                    "user": None,
                    "user_id": None,
                    "error": "This email already exists."
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

    new_user = {

        "user_id": next_user_id(users),

        "name": name,

        "email": email,

        "phone": phone,

        "password": password

    }

    users.append(new_user)

    save_users(users)

    return RedirectResponse(
        "/users/landing",
        status_code=status.HTTP_303_SEE_OTHER
    )
# ==========================
# Edit User
# ==========================

@router.get("/edit/{user_id}", response_class=HTMLResponse)
async def edit_user_form(request: Request, user_id: str):

    users = load_users()

    user = None

    for u in users:
        if u["user_id"] == user_id:
            user = u
            break

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
            "user": user,
            "user_id": user_id
        }
    )


@router.post("/{user_id}")
async def update_user(

    user_id: str,

    name: str = Form(...),

    email: str = Form(...),

    phone: str = Form(...),

    password: str = Form(...)

):

    users = load_users()

    for i, user in enumerate(users):

        if user["user_id"] == user_id:

            users[i] = {

                "user_id": user_id,

                "name": name,

                "email": email,

                "phone": phone,

                "password": password

            }

            save_users(users)

            return RedirectResponse(
                "/users/landing",
                status_code=status.HTTP_303_SEE_OTHER
            )

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
# ==========================
# Show Delete Page
# ==========================

@router.get("/delete/{user_id}", response_class=HTMLResponse)
async def confirm_delete(request: Request, user_id: str):

    users = load_users()

    user = None

    for u in users:
        if u["user_id"] == user_id:
            user = u
            break

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
async def delete_user(user_id: str):

    users = load_users()

    new_users = []

    for user in users:

        if user["user_id"] != user_id:
            new_users.append(user)

    if len(new_users) == len(users):
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    save_users(new_users)

    return RedirectResponse(
        "/users/landing",
        status_code=status.HTTP_303_SEE_OTHER
    )