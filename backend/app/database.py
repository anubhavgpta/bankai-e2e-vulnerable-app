import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "bankai_expenses.db"))


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'employee',
            display_name TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            receipt_path TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor_id INTEGER,
            action TEXT NOT NULL,
            expense_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    seed_users = [
        ("admin@bankai.local", "admin123", "admin", "Aizen Finance Admin"),
        ("employee@bankai.local", "password123", "employee", "Ichigo Kurosaki"),
        ("auditor@bankai.local", "audit123", "auditor", "Rukia Auditor"),
    ]
    for email, password, role, display_name in seed_users:
        cur.execute(
            "INSERT OR IGNORE INTO users (email, password, role, display_name) VALUES (?, ?, ?, ?)",
            (email, password, role, display_name),
        )

    cur.execute(
        """
        INSERT OR IGNORE INTO expenses
        (id, user_id, title, description, amount, category, status)
        VALUES (1, 2, 'Client dinner', 'Dinner with <strong>important</strong> enterprise prospect', 184.42, 'meals', 'pending')
        """
    )
    conn.commit()
    conn.close()


def row_to_dict(row):
    return dict(row) if row is not None else None
