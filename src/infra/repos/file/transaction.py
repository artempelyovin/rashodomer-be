import logging
from dataclasses import asdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from domain.errors import TransactionNotFoundError
from domain.models.transaction import Transaction, TransactionType
from domain.repos.transaction import TransactionRepo
from domain.utils import utc_now
from infra.repos.file.serializers import load_from_file, save_to_file

logger = logging.getLogger(__name__)


class TransactionFileRepo(TransactionRepo):
    def __init__(self, base_dir: Path = Path("data/transactions")) -> None:
        self._base_dir = base_dir
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def _file_path(self, transaction_id: str) -> Path:
        return self._base_dir / f"{transaction_id}.json"

    @staticmethod
    def _from_dict(data: dict[str, Any]) -> Transaction:
        # Convert string fields back to proper types
        data["amount"] = Decimal(data["amount"])
        data["type"] = TransactionType(data["type"])
        data["date"] = datetime.fromisoformat(data["date"])
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return Transaction(**data)

    async def create(self, transaction: Transaction) -> None:
        path = self._file_path(transaction.id)
        await save_to_file(path, asdict(transaction))
        logger.debug("Created transaction %s", transaction.id)

    async def get_by_id(self, transaction_id: str) -> Transaction | None:
        data = await load_from_file(self._file_path(transaction_id))
        return self._from_dict(data) if data else None

    async def get_by_user_id(self, user_id: str) -> list[Transaction]:
        result = []
        for path in self._base_dir.glob("*.json"):
            data = await load_from_file(path)
            if data and data.get("user_id") == user_id:
                result.append(self._from_dict(data))
        return result

    async def get_by_budget_id(self, budget_id: str) -> list[Transaction]:
        result = []
        for path in self._base_dir.glob("*.json"):
            data = await load_from_file(path)
            if data and data.get("budget_id") == budget_id:
                result.append(self._from_dict(data))
        return result

    async def update(self, transaction: Transaction) -> None:
        existing = await self.get_by_id(transaction.id)
        if existing is None:
            raise TransactionNotFoundError(transaction.id)
        transaction.updated_at = utc_now()
        await save_to_file(self._file_path(transaction.id), asdict(transaction))
        logger.debug("Updated transaction %s", transaction.id)

    async def delete(self, transaction_id: str) -> None:
        path = self._file_path(transaction_id)
        if not path.exists():
            raise TransactionNotFoundError(transaction_id)
        path.unlink()
        logger.debug("Deleted transaction %s", transaction_id)
