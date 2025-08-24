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
from models import Transaction
from repos.abc import CategoryRepo, Total, TransactionRepo
from settings import settings
from utils import utc_now


class TransactionManager:
    def __init__(
        self,
        transaction_repo: TransactionRepo = settings.transaction_repo,
        category_repo: CategoryRepo = settings.category_repo,
    ) -> None:
        self.transaction_repo = transaction_repo
        self.category_repo = category_repo

    async def create(
        self,
        user_id: str,
        amount: float,
        category_id: str,
        timestamp: datetime,
        description: str = "",
    ) -> Transaction:
        if amount <= 0:
            raise AmountMustBePositiveError
        category = await self.category_repo.get(category_id)
        if category is None:
            raise CategoryNotExistsError(category_id=category_id)
        if category.user_id != user_id:
            raise CategoryAccessDeniedError
        now = datetime.now(tz=UTC)
        if timestamp > now:
            raise TimestampInFutureError(timestamp=timestamp, current_timestamp=now)
        transaction = Transaction(
            amount=amount,
            description=description,
            category_id=category_id,
            timestamp=timestamp,
            user_id=user_id,
        )
        return await self.transaction_repo.add(transaction)

    async def get(self, user_id: str, transaction_id: str) -> Transaction:
        transaction = await self.transaction_repo.get(transaction_id)
        if not transaction:
            raise TransactionNotExistsError(transaction_id=transaction_id)
        if transaction.user_id != user_id:
            raise TransactionAccessDeniedError
        return transaction

    async def list_(self, user_id: str, *, limit: int | None, offset: int) -> tuple[Total, list[Transaction]]:
        return await self.transaction_repo.list_(user_id=user_id, limit=limit, offset=offset)

    async def update(
        self,
        user_id: str,
        transaction_id: str,
        amount: float,
        description: str,
        category_id: str,
        timestamp: datetime,
    ) -> Transaction:
        transaction = await self.transaction_repo.get(transaction_id)
        if not transaction:
            raise TransactionNotExistsError(transaction_id=transaction_id)
        if transaction.user_id != user_id:
            raise TransactionAccessDeniedError

        if amount <= 0:
            raise AmountMustBePositiveError
        transaction.amount = amount
        transaction.description = description
        
        category = await self.category_repo.get(category_id)
        if not category:
            raise CategoryNotExistsError(category_id=category_id)
        if category.user_id != user_id:
            raise CategoryAccessDeniedError
        transaction.category_id = category_id
        
        transaction.timestamp = timestamp
        transaction.updated_at = datetime.now(tz=UTC)
        return await self.transaction_repo.update(transaction)

    async def delete(self, user_id: str, transaction_id: str) -> Transaction:
        transaction = await self.transaction_repo.get(transaction_id)
        if not transaction:
            raise TransactionNotExistsError(transaction_id=transaction_id)
        if transaction.user_id != user_id:
            raise TransactionAccessDeniedError
        return await self.transaction_repo.delete(transaction_id)

    async def find(
        self, user_id: str, text: str, *, case_sensitive: bool, limit: int | None, offset: int
    ) -> tuple[Total, list[Transaction]]:
        if len(text) == 0:
            raise EmptySearchTextError
        return await self.transaction_repo.find_by_text(
            user_id=user_id, text=text, case_sensitive=case_sensitive, limit=limit, offset=offset
        )
