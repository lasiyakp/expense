from expense_tracker.models.expense import Expense


class ConsoleView:
    """Responsible for rendering data to the console."""

    @staticmethod
    def show_expense_added(expense: Expense) -> None:
        print(
            f"Added expense: {expense.title} | ${expense.amount:.2f} | "
            f"Category: {expense.category}"
        )

    @staticmethod
    def show_expense_list(expenses: list[Expense]) -> None:
        if not expenses:
            print("No expenses recorded yet.")
            return

        print("\nExpenses")
        print("-" * 50)
        for idx, expense in enumerate(expenses, start=1):
            print(
                f"{idx}. {expense.title:<18} ${expense.amount:>8.2f} "
                f"[{expense.category}]"
            )

    @staticmethod
    def show_total(total: float) -> None:
        print(f"\nTotal spending: ${total:.2f}")
