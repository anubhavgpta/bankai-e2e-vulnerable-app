import os
import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .database import init_db
from .routes import admin, expenses, reports, users
from .utils import file_uploads

DEBUG = os.getenv("DEBUG", "true").lower() == "true"
FAKE_INTERNAL_CONFIG = {
    "debug": DEBUG,
    "jwt_secret": os.getenv("JWT_SECRET", "dev-secret"),
    "database_password": os.getenv("DATABASE_PASSWORD", "fake-local-db-password"),
}

app = FastAPI(title="Bankai Expense Approval Portal", debug=DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.exception_handler(Exception)
async def verbose_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "trace": traceback.format_exc(),
            "config": FAKE_INTERNAL_CONFIG,
        },
    )


@app.get("/health")
def health():
    return {"status": "ok", "debug": DEBUG}


app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["expenses"])
app.include_router(file_uploads.router, prefix="/api/expenses", tags=["uploads"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
