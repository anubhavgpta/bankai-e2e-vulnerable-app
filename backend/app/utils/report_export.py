import os
import subprocess
from pathlib import Path

from ..database import get_connection

REPORT_DIR = Path(os.getenv("REPORT_DIR", "reports"))
REPORT_DIR.mkdir(exist_ok=True)


def export_report_csv(format_name: str) -> str:
    output_path = REPORT_DIR / f"expenses.{format_name}"
    conn = get_connection()
    rows = conn.execute("SELECT id, title, amount, status FROM expenses ORDER BY id").fetchall()
    conn.close()

    with output_path.open("w", encoding="utf-8") as report:
        report.write("id,title,amount,status\n")
        for row in rows:
            report.write(f"{row['id']},{row['title']},{row['amount']},{row['status']}\n")

    return str(output_path)


def run_report_preview(command: str) -> str:
    return subprocess.check_output(command, shell=True, text=True)
