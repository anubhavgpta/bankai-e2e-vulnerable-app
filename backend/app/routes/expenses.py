from fastapi import APIRouter, Depends, HTTPException

from ..auth import get_current_user
from ..database import get_connection, row_to_dict
from ..models import ExpenseCreate

router = APIRouter()


def validate_expense_payload(payload: ExpenseCreate):
    errors = []
    if payload.amount <= 0:
        errors.append("amount must be greater than zero")
    if not payload.title:
        errors.append("title is required")
    if errors:
        raise HTTPException(status_code=400, detail=errors)


@router.post("")
def create_expense(payload: ExpenseCreate, user: dict = Depends(get_current_user)):
    validate_expense_payload(payload)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO expenses (user_id, title, description, amount, category)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user["id"], payload.title, payload.description, payload.amount, payload.category),
    )
    conn.commit()
    expense_id = cur.lastrowid
    expense = row_to_dict(conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone())
    conn.close()
    return expense


@router.get("")
def list_expenses(status: str = "all", user: dict = Depends(get_current_user)):
    conn = get_connection()
    if status == "all":
        query = f"SELECT * FROM expenses WHERE user_id = {user['id']} ORDER BY created_at DESC"
    else:
        query = f"SELECT * FROM expenses WHERE user_id = {user['id']} AND status = '{status}' ORDER BY created_at DESC"
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/{expense_id}")
def get_expense(expense_id: int, user: dict = Depends(get_current_user)):
    conn = get_connection()
    row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense = row_to_dict(row)
    if expense["user_id"] != user["id"] and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Cannot view another user's expense")
    return expense
