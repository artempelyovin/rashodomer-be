from datetime import UTC, datetime

from exceptions import (
    AmountMustBePositiveError,
    CategoryAccessDeniedError,
    CategoryNotExistsError,
    TimestampInFutureError, TransactionNotExistsError, TransactionAccessDeniedError,
)
from repos.abc import CategoryRepo, TransactionRepo
from schemas.transaction import CreateTransactionSchema, TransactionSchema


class TransactionManager:
    def __init__(self, transaction_repo: TransactionRepo, category_repo: CategoryRepo) -> None:
        self.transaction_repo = transaction_repo
        self.category_repo = category_repo

    async def create(self, user_id: str, data: CreateTransactionSchema) -> TransactionSchema:
        if data.amount <= 0:
            raise AmountMustBePositiveError
        category = await self.category_repo.get(data.category_id)
        if category is None:
            raise CategoryNotExistsError(category_id=data.category_id)
        if category.user_id != user_id:
            raise CategoryAccessDeniedError
        now = datetime.now(tz=UTC)
        if data.timestamp > now:
            raise TimestampInFutureError(timestamp=data.timestamp, current_timestamp=now)
        transaction = TransactionSchema(
            amount=data.amount,
            description=data.description,
            category_id=data.category_id,
            timestamp=data.timestamp,
            user_id=user_id,
        )
        return await self.transaction_repo.add(transaction)

    async def get(self, user_id: str, transaction_id: str) -> TransactionSchema:
        transaction = await self.transaction_repo.get(transaction_id)
        if not transaction:
            raise TransactionNotExistsError(transaction_id=transaction_id)
        if transaction.user_id != user_id:
            raise TransactionAccessDeniedError
        return transaction
