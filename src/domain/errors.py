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
