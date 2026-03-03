from expense_tracker.app import AppConfig
from expense_tracker.controllers.expense_controller import ExpenseController
from expense_tracker.factories.repository_factory import RepositoryFactory


def test_singleton_config_returns_same_instance():
    config_a = AppConfig(storage_type="memory")
    config_b = AppConfig(storage_type="file", file_path="ignored.json")

    assert config_a is config_b
    assert config_b.storage_type == "memory"


def test_factory_creates_memory_repository():
    repository = RepositoryFactory.create("memory")
    controller = ExpenseController(repository)

    controller.create_expense("Coffee", 4.5, "Food")
    expenses = controller.get_expenses()

    assert len(expenses) == 1
    assert expenses[0].title == "Coffee"


def test_controller_total_spend_is_computed_correctly():
    repository = RepositoryFactory.create("memory")
    controller = ExpenseController(repository)

    controller.create_expense("Book", 15.0, "Education")
    controller.create_expense("Pen", 2.0, "Education")

    assert controller.get_total_spend() == 17.0
