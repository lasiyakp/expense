from __future__ import annotations

from collections import defaultdict
from html import escape
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from expense_tracker.controllers.expense_controller import ExpenseController
from expense_tracker.factories.repository_factory import RepositoryFactory


class DashboardApp:
    """Small WSGI dashboard app using only the standard library."""

    def __init__(self, storage_type: str = "file", file_path: str = "expenses.json") -> None:
        repository = RepositoryFactory.create(storage_type=storage_type, file_path=file_path)
        self.controller = ExpenseController(repository)

    def __call__(self, environ, start_response):
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")

        if method == "POST" and path == "/expenses":
            return self._handle_create_expense(environ, start_response)

        if method == "GET" and path == "/":
            html = self._render_dashboard()
            start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
            return [html.encode("utf-8")]

        start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"Not Found"]

    def _handle_create_expense(self, environ, start_response):
        size = int(environ.get("CONTENT_LENGTH") or 0)
        raw_body = environ["wsgi.input"].read(size).decode("utf-8")
        data = parse_qs(raw_body)

        title = data.get("title", [""])[0].strip()
        category = data.get("category", [""])[0].strip() or "Other"
        amount_raw = data.get("amount", [""])[0].strip()

        if title and amount_raw:
            try:
                amount = float(amount_raw)
            except ValueError:
                amount = -1

            if amount >= 0:
                self.controller.create_expense(title=title, amount=amount, category=category)

        start_response("303 See Other", [("Location", "/")])
        return [b""]

    def _render_dashboard(self) -> str:
        expenses = self.controller.get_expenses()
        total_spend = self.controller.get_total_spend()
        total_count = len(expenses)
        avg_spend = total_spend / total_count if total_count else 0.0

        category_totals: dict[str, float] = defaultdict(float)
        for expense in expenses:
            category_totals[expense.category] += expense.amount

        category_rows = "".join(
            f"<li class='list-group-item d-flex justify-content-between px-0'><span>{escape(cat)}</span><strong>${total:.2f}</strong></li>"
            for cat, total in sorted(category_totals.items())
        )
        if not category_rows:
            category_rows = "<p class='text-secondary mb-0'>No category data yet.</p>"

        expense_rows = "".join(
            (
                "<tr>"
                f"<td>{idx}</td>"
                f"<td>{escape(expense.title)}</td>"
                f"<td><span class='badge text-bg-light'>{escape(expense.category)}</span></td>"
                f"<td class='text-end fw-semibold'>${expense.amount:.2f}</td>"
                "</tr>"
            )
            for idx, expense in enumerate(reversed(expenses), start=1)
        )
        if not expense_rows:
            expense_rows = "<tr><td colspan='4' class='text-secondary'>No expenses added yet.</td></tr>"

        return f"""<!doctype html>
<html lang='en'>
  <head>
    <meta charset='UTF-8' />
    <meta name='viewport' content='width=device-width, initial-scale=1.0' />
    <title>Expense Dashboard</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet' />
    <style>
      body {{ background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%); min-height: 100vh; }}
      .stat-card {{ border-left: 4px solid #6366f1; }}
    </style>
  </head>
  <body>
    <div class='container py-4'>
      <header class='mb-4'>
        <h1 class='h3 fw-bold mb-1'>Expense Dashboard</h1>
        <p class='text-secondary mb-0'>Professional overview of your spending</p>
      </header>

      <section class='row g-3 mb-4'>
        <div class='col-md-4'><div class='card stat-card border-0 shadow-sm h-100'><div class='card-body'><p class='text-secondary mb-1'>Total Spending</p><h2 class='h4 mb-0'>${total_spend:.2f}</h2></div></div></div>
        <div class='col-md-4'><div class='card stat-card border-0 shadow-sm h-100'><div class='card-body'><p class='text-secondary mb-1'>Expenses Logged</p><h2 class='h4 mb-0'>{total_count}</h2></div></div></div>
        <div class='col-md-4'><div class='card stat-card border-0 shadow-sm h-100'><div class='card-body'><p class='text-secondary mb-1'>Average Expense</p><h2 class='h4 mb-0'>${avg_spend:.2f}</h2></div></div></div>
      </section>

      <section class='row g-4'>
        <div class='col-lg-4'>
          <div class='card border-0 shadow-sm mb-4'><div class='card-body'>
            <h3 class='h5 mb-3'>Add Expense</h3>
            <form method='post' action='/expenses' class='row g-2'>
              <div class='col-12'><input class='form-control' type='text' name='title' placeholder='Title' required /></div>
              <div class='col-12'><input class='form-control' type='number' step='0.01' min='0' name='amount' placeholder='Amount' required /></div>
              <div class='col-12'><input class='form-control' type='text' name='category' placeholder='Category' /></div>
              <div class='col-12'><button class='btn btn-primary w-100' type='submit'>Save Expense</button></div>
            </form>
          </div></div>

          <div class='card border-0 shadow-sm'><div class='card-body'><h3 class='h5 mb-3'>Category Breakdown</h3><ul class='list-group list-group-flush'>{category_rows}</ul></div></div>
        </div>

        <div class='col-lg-8'>
          <div class='card border-0 shadow-sm'><div class='card-body'>
            <h3 class='h5 mb-3'>Recent Expenses</h3>
            <div class='table-responsive'>
              <table class='table align-middle'>
                <thead><tr><th>#</th><th>Title</th><th>Category</th><th class='text-end'>Amount</th></tr></thead>
                <tbody>{expense_rows}</tbody>
              </table>
            </div>
          </div></div>
        </div>
      </section>
    </div>
  </body>
</html>"""


def create_app(storage_type: str = "file", file_path: str = "expenses.json") -> DashboardApp:
    return DashboardApp(storage_type=storage_type, file_path=file_path)


if __name__ == "__main__":
    app = create_app()
    with make_server("0.0.0.0", 5000, app) as server:
        print("Serving dashboard at http://0.0.0.0:5000")
        server.serve_forever()
