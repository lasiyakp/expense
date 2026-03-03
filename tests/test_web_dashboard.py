from io import BytesIO
from pathlib import Path

from expense_tracker.web_app import create_app


def _invoke_app(app, method: str, path: str, body: bytes = b""):
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = headers

    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "CONTENT_LENGTH": str(len(body)),
        "wsgi.input": BytesIO(body),
    }

    response_body = b"".join(app(environ, start_response))
    return captured["status"], dict(captured["headers"]), response_body


def test_dashboard_renders_summary_cards(tmp_path: Path):
    app = create_app(storage_type="file", file_path=str(tmp_path / "expenses.json"))

    status, _, body = _invoke_app(app, "GET", "/")

    assert status.startswith("200")
    assert b"Expense Dashboard" in body
    assert b"Total Spending" in body


def test_add_expense_updates_dashboard(tmp_path: Path):
    app = create_app(storage_type="file", file_path=str(tmp_path / "expenses.json"))

    status, headers, _ = _invoke_app(
        app,
        "POST",
        "/expenses",
        body=b"title=Groceries&amount=45.50&category=Food",
    )

    assert status.startswith("303")
    assert headers["Location"] == "/"

    _, _, dashboard = _invoke_app(app, "GET", "/")
    assert b"Groceries" in dashboard
    assert b"$45.50" in dashboard
    assert b"Food" in dashboard
