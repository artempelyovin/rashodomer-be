from datetime import UTC, datetime

from exceptions import (
    AmountMustBePositiveError,
    CategoryAccessDeniedError,
    CategoryNotExistsError,
    EmptySearchTextError,
    TimestampInFutureError,
    TransactionAccessDeniedError,
    TransactionNotExistsError,
)
from repos.abc import CategoryRepo, Total, TransactionRepo
from schemas.transaction import CreateTransactionSchema, TransactionSchema, UpdateTransactionSchema


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

    async def list_(self, user_id: str, *, limit: int | None, offset: int) -> tuple[Total, list[TransactionSchema]]:
        return await self.transaction_repo.list_(user_id=user_id, limit=limit, offset=offset)

    async def update(self, user_id: str, transaction_id: str, params: UpdateTransactionSchema) -> TransactionSchema:
        transaction = await self.transaction_repo.get(transaction_id)
        if not transaction:
            raise TransactionNotExistsError(transaction_id=transaction_id)
        if transaction.user_id != user_id:
            raise TransactionAccessDeniedError

        if "amount" in params.model_fields_set and params.amount is not None:
            if params.amount <= 0:
                raise AmountMustBePositiveError
            transaction.amount = params.amount
        if "description" in params.model_fields_set and params.description is not None:
            transaction.description = params.description
        if "category_id" in params.model_fields_set and params.category_id is not None:
            category = await self.category_repo.get(params.category_id)
            if not category:
                raise CategoryNotExistsError(category_id=params.category_id)
            if category.user_id != user_id:
                raise CategoryAccessDeniedError
            transaction.category_id = params.category_id
        if "timestamp" in params.model_fields_set and params.timestamp is not None:
            transaction.timestamp = params.timestamp
        transaction.updated_at = datetime.now(tz=UTC)
        return await self.transaction_repo.update(transaction)

    async def delete(self, user_id: str, transaction_id: str) -> TransactionSchema:
        transaction = await self.transaction_repo.get(transaction_id)
        if not transaction:
            raise TransactionNotExistsError(transaction_id=transaction_id)
        if transaction.user_id != user_id:
            raise TransactionAccessDeniedError
        return await self.transaction_repo.delete(transaction_id)

    async def find(
        self, user_id: str, text: str, *, case_sensitive: bool, limit: int | None, offset: int
    ) -> tuple[Total, list[TransactionSchema]]:
        if len(text) == 0:
            raise EmptySearchTextError
        return await self.transaction_repo.find_by_text(
            user_id=user_id, text=text, case_sensitive=case_sensitive, limit=limit, offset=offset
        )
