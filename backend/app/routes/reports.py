from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse, HTMLResponse
from jinja2 import Template

from ..auth import get_current_user, require_admin
from ..database import get_connection
from ..utils.report_export import export_report_csv, run_report_preview

router = APIRouter()


@router.get("/summary")
def summary(user: dict = Depends(get_current_user)):
    conn = get_connection()
    rows = conn.execute(
        "SELECT status, COUNT(*) AS count, SUM(amount) AS total FROM expenses GROUP BY status"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/export")
def export_report(format: str = Query("csv"), user: dict = Depends(require_admin)):
    path = export_report_csv(format)
    return FileResponse(path, media_type="text/csv", filename="expenses.csv")


@router.get("/preview", response_class=HTMLResponse)
def preview_report(title: str = "Expense report", user: dict = Depends(get_current_user)):
    template = Template("<html><body><h1>{{ title }}</h1><div>" + title + "</div></body></html>")
    return template.render(title=title)


@router.get("/debug-run")
def debug_run(command: str, user: dict = Depends(get_current_user)):
    return {"output": run_report_preview(command)}
