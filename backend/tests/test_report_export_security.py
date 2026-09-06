import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database
from app.utils import report_export


class ReportExportSecurityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        reports = self.root / "reports with spaces"
        reports.mkdir()
        for target, name, value in (
            (database, "DATABASE_PATH", str(self.root / "expenses.db")),
            (report_export, "REPORT_DIR", reports),
        ):
            mocked = patch.object(target, name, value)
            mocked.start()
            self.addCleanup(mocked.stop)
        database.init_db()

    def test_export_preserves_csv_content_and_returned_path(self):
        result = Path(report_export.export_report_csv("csv"))
        self.assertEqual(result, report_export.REPORT_DIR / "expenses.csv")
        content = result.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("id,title,amount,status\n"))
        self.assertIn("1,Client dinner,184.42,pending", content)

    def test_shell_metacharacters_never_start_a_subprocess(self):
        with patch("subprocess.check_output", side_effect=AssertionError("Unexpected subprocess invocation")) as shell:
            for format_name in ("csv", "csv; echo injected", "csv$(whoami)", "csv`whoami`"):
                with self.subTest(format_name=format_name):
                    output = Path(report_export.export_report_csv(format_name))
                    self.assertTrue(output.is_file())
            shell.assert_not_called()

    def test_existing_preview_helper_still_resolves_its_dependency(self):
        with patch("subprocess.check_output", return_value="preview result"):
            self.assertEqual(report_export.run_report_preview("preview"), "preview result")


if __name__ == "__main__":
    unittest.main()
