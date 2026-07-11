from datetime import datetime, timedelta

from jose import jwt
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

# برای Hash کردن رمزها
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# کلید JWT (بعداً می‌توانیم داخل .env قرارش بدهیم)
SECRET_KEY = "gallerycar_secret_key_2026"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 43200

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/api/login"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print(payload)

        return payload

    except JWTError as e:
        print(e)
        return None
    
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    print("TOKEN =", token)
    payload = decode_token(token)
    print("PAYLOAD =", payload)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user