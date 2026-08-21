from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    role: str
    display_name: str


class ExpenseCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    amount: float
    category: str


class ExpenseOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    amount: float
    category: str
    status: str
    receipt_path: Optional[str] = None


class ApprovalRequest(BaseModel):
    status: str
    note: Optional[str] = ""
