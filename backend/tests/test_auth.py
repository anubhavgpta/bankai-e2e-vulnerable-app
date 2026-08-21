from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_returns_token_for_seed_user():
    response = client.post(
        "/api/users/login",
        json={"email": "employee@bankai.local", "password": "password123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["user"]["role"] == "employee"


def test_admin_route_rejects_employee_token():
    login = client.post(
        "/api/users/login",
        json={"email": "employee@bankai.local", "password": "password123"},
    )
    token = login.json()["access_token"]

    response = client.get(
        "/api/admin/expenses",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


def test_sql_injection_login_bypasses_password_check():
    response = client.post(
        "/api/users/login",
        json={"email": "employee@bankai.local' --", "password": "not-the-password"},
    )

    assert response.status_code == 200
