# Bankai E2E Vulnerable App

A deliberately imperfect internal expense approval portal for end-to-end testing of security remediation platforms.

This repository is intentionally built like a small production app: FastAPI backend, React + Vite frontend, SQLite database, Docker support, CI, and tests. It also intentionally contains many realistic security issues for scanners and remediation agents to detect.

All secrets and credentials in this repository are fake and harmless.

## Features

- User login with JWT tokens
- Expense submission and receipt uploads
- Admin approval dashboard
- Expense reports and CSV export
- SQLite persistence
- Docker Compose local stack
- GitHub Actions CI

## Repository Layout

```text
backend/      FastAPI API, SQLite models, routes, tests
frontend/     React + Vite UI
.github/      CI workflow
```

## Local Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

On Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000`.

## Docker

```bash
docker compose up --build
```

Backend: `http://localhost:8000`  
Frontend: `http://localhost:5173`

## Demo Accounts

The app seeds the following fake accounts on startup:

| Role | Email | Password |
| --- | --- | --- |
| Admin | `admin@bankai.local` | `admin123` |
| User | `employee@bankai.local` | `password123` |
| User | `auditor@bankai.local` | `audit123` |

## Tests

```bash
cd backend
pytest
```

The test suite includes one skipped test documenting a known policy gap around receipt file validation.

## Deployment Notes

This app is not intended for production deployment. For a hardened version, replace the included fake secrets, lock down CORS, add proper password hashing, add rate limiting, validate uploads, use parameterized SQL consistently, run containers as a non-root user, and scope CI permissions to least privilege.

## Security Testing Scope

This repository intentionally includes examples of:

- Outdated dependency pins
- Fake secret exposure
- SQL injection and command injection risks
- Authentication and authorization flaws
- Unsafe file uploads
- Weak API security configuration
- Frontend unsafe rendering
- Insecure Docker and CI configuration
- Code quality issues suitable for automated remediation

It also includes safe examples, including a parameterized SQL query, an authorization-protected endpoint, safe frontend rendering, and a test covering expected auth behavior.
