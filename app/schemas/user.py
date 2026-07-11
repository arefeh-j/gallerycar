from pydantic import BaseModel


class UserBase(BaseModel):
    full_name: str
    email: str
    phone: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    password: str | None = None


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

# ========== اضافه کن ==========
class RegisterRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str
    role: str = "user"   # مقدار پیش‌فرض: کاربر عادی