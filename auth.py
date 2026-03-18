"""JWT auth and password hashing."""
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET  = os.getenv("JWT_SECRET", "change_me_in_production_please")
ALGO    = "HS256"
EXPIRE  = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)


def create_token(data: dict) -> str:
    payload = {**data, "exp": datetime.utcnow() + timedelta(minutes=EXPIRE)}
    return jwt.encode(payload, SECRET, algorithm=ALGO)


def verify_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGO])
    except JWTError:
        return None
