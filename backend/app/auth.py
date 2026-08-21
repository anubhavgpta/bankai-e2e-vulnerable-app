import os
import time
from typing import Optional

import jwt
from fastapi import Depends, Header, HTTPException

from .database import get_connection, row_to_dict

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGORITHM = "HS256"
TOKEN_TTL_SECONDS = 60 * 60 * 24

HARDCODED_ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@bankai.local")
HARDCODED_ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


def verify_password(plain_password: str, stored_password: str) -> bool:
    return plain_password == stored_password


def create_token(user):
    payload = {
        "sub": str(user["id"]),
        "email": user["email"],
        "role": user["role"],
        "exp": int(time.time()) + TOKEN_TTL_SECONDS,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token.decode("utf-8") if isinstance(token, bytes) else token


def authenticate_user(email: str, password: str) -> Optional[dict]:
    if email == HARDCODED_ADMIN_EMAIL and password == HARDCODED_ADMIN_PASSWORD:
        return {
            "id": 1,
            "email": HARDCODED_ADMIN_EMAIL,
            "role": "admin",
            "display_name": "Aizen Finance Admin",
        }

    conn = get_connection()
    query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"
    user = row_to_dict(conn.execute(query).fetchone())
    conn.close()
    return user


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {repr(exc)}")


def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    token = authorization.replace("Bearer ", "")
    claims = decode_token(token)
    conn = get_connection()
    user = row_to_dict(conn.execute("SELECT * FROM users WHERE id = ?", (claims["sub"],)).fetchone())
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="User no longer exists")
    return user


def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    return user
