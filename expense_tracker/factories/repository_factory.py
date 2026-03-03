from expense_tracker.storage.repository import (
    ExpenseRepository,
    FileExpenseRepository,
    InMemoryExpenseRepository,
)


class RepositoryFactory:
    """Factory for creating repository implementations."""

    @staticmethod
    def create(storage_type: str = "memory", **kwargs) -> ExpenseRepository:
        storage = storage_type.lower()
        if storage == "memory":
            return InMemoryExpenseRepository()
        if storage == "file":
            return FileExpenseRepository(file_path=kwargs.get("file_path", "expenses.json"))
        raise ValueError(f"Unsupported storage type: {storage_type}")
