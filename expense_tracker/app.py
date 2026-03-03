from __future__ import annotations

from expense_tracker.controllers.expense_controller import ExpenseController
from expense_tracker.factories.repository_factory import RepositoryFactory
from expense_tracker.views.console_view import ConsoleView


class AppConfig:
    """Singleton config used to share runtime settings."""

    _instance: AppConfig | None = None

    def __new__(cls, storage_type: str = "memory", file_path: str = "expenses.json") -> "AppConfig":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.storage_type = storage_type
            cls._instance.file_path = file_path
        return cls._instance


class ExpenseTrackerApp:
    """Wires MVC components and orchestrates app flow."""

    def __init__(self, config: AppConfig) -> None:
        repository = RepositoryFactory.create(
            storage_type=config.storage_type,
            file_path=config.file_path,
        )
        self.controller = ExpenseController(repository)
        self.view = ConsoleView()

    def run_demo(self) -> None:
        sample_expenses = [
            ("Lunch", 12.5, "Food"),
            ("Bus Ticket", 3.0, "Transport"),
            ("Notebook", 7.25, "Supplies"),
        ]

        for title, amount, category in sample_expenses:
            expense = self.controller.create_expense(title, amount, category)
            self.view.show_expense_added(expense)

        expenses = self.controller.get_expenses()
        total = self.controller.get_total_spend()

        self.view.show_expense_list(expenses)
        self.view.show_total(total)


if __name__ == "__main__":
    config = AppConfig(storage_type="memory")
    app = ExpenseTrackerApp(config)
    app.run_demo()
