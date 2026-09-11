import os
from pathlib import Path

from ..database import get_connection

REPORT_DIR = Path(os.getenv("REPORT_DIR", "reports"))
REPORT_DIR.mkdir(exist_ok=True)


def export_report_csv(format_name: str) -> str:
    if format_name != "csv":
        raise ValueError("Unsupported report format")
    output_path = REPORT_DIR / "expenses.csv"
    conn = get_connection()
    rows = conn.execute("SELECT id, title, amount, status FROM expenses ORDER BY id").fetchall()
    conn.close()

    with output_path.open("w", encoding="utf-8") as report:
        report.write("id,title,amount,status\n")
        for row in rows:
            report.write(f"{row['id']},{row['title']},{row['amount']},{row['status']}\n")

    return str(output_path)


def run_report_preview(command: str) -> str:
    if command != "csv":
        raise ValueError("Unsupported preview command")
    output_path = export_report_csv(command)
    return Path(output_path).read_text(encoding="utf-8")
