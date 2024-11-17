from datetime import datetime

from core.entities import Transaction
from core.enums import TransactionType
from core.exceptions import (
    AmountMustBePositiveError,
    BudgetAccessDeniedError,
    BudgetNotExistsError,
    CategoryAccessDeniedError,
    CategoryNotExistsError,
    UnsupportedTransactionTypeError,
)
from core.services import BudgetService, CategoryService, TransactionService


class CreateTransactionUseCase:
    def __init__(
        self, budget_service: BudgetService, category_service: CategoryService, transaction_service: TransactionService
    ) -> None:
        self._category_repo = category_service
        self._budget_repo = budget_service
        self._transaction_repo = transaction_service

    async def create(
        self,
        user_id: str,
        amount: float,
        description: str,
        transaction_type: TransactionType,
        budget_id: str,
        category_id: str,
        timestamp: datetime,
    ) -> Transaction:
        if amount < 0:
            raise AmountMustBePositiveError
        budget = await self._budget_repo.get(budget_id)
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        category = await self._category_repo.get(category_id)
        if not category:
            raise CategoryNotExistsError(category_id=category_id)
        if category.user_id != user_id:
            raise CategoryAccessDeniedError
        transaction = await self._transaction_repo.create(
            amount=amount,
            description=description,
            transaction_type=transaction_type,
            budget_id=budget_id,
            category_id=category_id,
            user_id=user_id,
            timestamp=timestamp,
        )
        match transaction_type:
            case TransactionType.EXPENSE:
                new_budget_amount = budget.amount - transaction.amount
            case TransactionType.EXPENSE:
                new_budget_amount = budget.amount - transaction.amount
            case _:
                raise UnsupportedTransactionTypeError(transaction_type=transaction_type)
        await self._budget_repo.update_budget(budget_id=budget_id, amount=new_budget_amount)
        return transaction
