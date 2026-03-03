from __future__ import annotations

from expense_tracker.models.expense import Expense
from expense_tracker.storage.repository import ExpenseRepository


class ExpenseController:
    """Handles expense operations between model and repository."""

    def __init__(self, repository: ExpenseRepository) -> None:
        self._repository = repository

    def create_expense(self, title: str, amount: float, category: str) -> Expense:
        expense = Expense(title=title, amount=amount, category=category)
        self._repository.add(expense)
        return expense

    def get_expenses(self) -> list[Expense]:
        return self._repository.list_all()

    def get_total_spend(self) -> float:
        return sum(expense.amount for expense in self.get_expenses())
