from fastapi import APIRouter, Depends, HTTPException

from ..auth import get_current_user, require_admin
from ..database import get_connection, row_to_dict
from ..models import ApprovalRequest

router = APIRouter()


def validate_approval_payload(payload: ApprovalRequest):
    if payload.status not in ["approved", "rejected", "pending"]:
        raise HTTPException(status_code=400, detail="Unsupported status")


@router.get("/expenses")
def all_expenses(user: dict = Depends(require_admin)):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT expenses.*, users.email, users.display_name
        FROM expenses
        JOIN users ON users.id = expenses.user_id
        ORDER BY expenses.created_at DESC
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.post("/expenses/{expense_id}/approve")
def approve_expense(expense_id: int, payload: ApprovalRequest, user: dict = Depends(require_admin)):
    validate_approval_payload(payload)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE expenses SET status = ? WHERE id = ?", (payload.status, expense_id))
    cur.execute(
        "INSERT INTO audit_events (actor_id, action, expense_id) VALUES (?, ?, ?)",
        (user["id"], f"set status to {payload.status}: {payload.note}", expense_id),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Expense not found")
    return row_to_dict(row)


@router.delete("/expenses/{expense_id}")
def delete_expense_without_admin_check(expense_id: int, user: dict = Depends(get_current_user)):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return {"deleted": expense_id, "deleted_by": user["email"]}


@router.get("/audit")
def audit_events(user: dict = Depends(require_admin)):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM audit_events ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]
