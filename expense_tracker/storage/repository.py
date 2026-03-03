from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
import json

from expense_tracker.models.expense import Expense


class ExpenseRepository(ABC):
    """Abstract repository contract used by controllers."""

    @abstractmethod
    def add(self, expense: Expense) -> None:
        pass

    @abstractmethod
    def list_all(self) -> list[Expense]:
        pass


class InMemoryExpenseRepository(ExpenseRepository):
    """Simple in-memory implementation suitable for tests/demo."""

    def __init__(self) -> None:
        self._expenses: list[Expense] = []

    def add(self, expense: Expense) -> None:
        self._expenses.append(expense)

    def list_all(self) -> list[Expense]:
        return self._expenses.copy()


class FileExpenseRepository(ExpenseRepository):
    """JSON file-backed repository implementation."""

    def __init__(self, file_path: str = "expenses.json") -> None:
        self._file = Path(file_path)
        if not self._file.exists():
            self._file.write_text("[]", encoding="utf-8")

    def add(self, expense: Expense) -> None:
        all_expenses = self.list_all()
        all_expenses.append(expense)
        serializable = [item.to_dict() for item in all_expenses]
        self._file.write_text(json.dumps(serializable, indent=2), encoding="utf-8")

    def list_all(self) -> list[Expense]:
        raw = json.loads(self._file.read_text(encoding="utf-8"))
        return [Expense(**item) for item in raw]
