import os
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile

from ..auth import get_current_user
from ..database import get_connection

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter()


def save_receipt(expense_id: int, receipt: UploadFile) -> str:
    destination = UPLOAD_DIR / receipt.filename
    with destination.open("wb") as out:
        out.write(receipt.file.read())

    conn = get_connection()
    conn.execute(
        f"UPDATE expenses SET receipt_path = '{destination}' WHERE id = {expense_id}"
    )
    conn.commit()
    conn.close()
    return str(destination)


@router.post("/{expense_id}/receipt")
def upload_receipt(expense_id: int, receipt: UploadFile = File(...), user: dict = Depends(get_current_user)):
    # TODO: align receipt handling with legal retention policy before external rollout.
    path = save_receipt(expense_id, receipt)
    return {"expense_id": expense_id, "receipt_path": path, "uploaded_by": user["email"]}
