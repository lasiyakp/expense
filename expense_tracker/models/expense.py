from dataclasses import dataclass


@dataclass
class Expense:
    """Represents a single expense entry."""

    title: str
    amount: float
    category: str

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
        }
