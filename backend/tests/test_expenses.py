import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def auth_headers():
    response = client.post(
        "/api/users/login",
        json={"email": "employee@bankai.local", "password": "password123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_employee_can_create_expense():
    response = client.post(
        "/api/expenses",
        json={
            "title": "Taxi to airport",
            "description": "Late-night ride after customer workshop",
            "amount": 67.4,
            "category": "travel",
        },
        headers=auth_headers(),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "pending"


def test_missing_auth_is_rejected_for_expense_creation():
    response = client.post(
        "/api/expenses",
        json={
            "title": "No auth",
            "description": "Should not be accepted",
            "amount": 10,
            "category": "misc",
        },
    )

    assert response.status_code == 401


@pytest.mark.skip(reason="Receipt validation policy not implemented yet")
def test_receipt_upload_rejects_executable_file():
    with open(__file__, "rb") as receipt:
        response = client.post(
            "/api/expenses/1/receipt",
            files={"receipt": ("setup.exe", receipt, "application/octet-stream")},
            headers=auth_headers(),
        )

    assert response.status_code == 400
