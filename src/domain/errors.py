from decimal import Decimal


class DomainError(Exception):
    """Base exception for all domain errors."""


class BudgetNotFoundError(DomainError):
    def __init__(self, budget_id: str) -> None:
        super().__init__(f"Budget with id '{budget_id}' not found")


class CategoryNotFoundError(DomainError):
    def __init__(self, category_id: str) -> None:
        super().__init__(f"Category with id '{category_id}' not found")


class TransactionNotFoundError(DomainError):
    def __init__(self, transaction_id: str) -> None:
        super().__init__(f"Transaction with id '{transaction_id}' not found")


class NegativeBalanceError(DomainError):
    def __init__(self, balance: Decimal) -> None:
        super().__init__(f"Balance cannot be negative: {balance}")


class EmptyNameError(DomainError):
    def __init__(self, field: str = "name") -> None:
        super().__init__(f"{field.capitalize()} cannot be empty")
