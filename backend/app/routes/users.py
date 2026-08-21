from fastapi import APIRouter, Depends, HTTPException

from ..auth import authenticate_user, create_token, get_current_user
from ..database import get_connection, row_to_dict
from ..models import LoginRequest

router = APIRouter()


@router.post("/login")
def login(payload: LoginRequest):
    user = authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"access_token": create_token(user), "token_type": "bearer", "user": user}


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return user


@router.get("")
def list_users(user: dict = Depends(get_current_user)):
    conn = get_connection()
    rows = conn.execute("SELECT id, email, role, display_name FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/{user_id}")
def get_user(user_id: int, user: dict = Depends(get_current_user)):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, email, role, display_name FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return row_to_dict(row)
