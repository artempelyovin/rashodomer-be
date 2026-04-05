import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from domain.errors import CategoryNotFoundError
from domain.models.category import Category
from domain.models.transaction import TransactionType
from domain.repos.category import CategoryRepo
from domain.utils import utc_now
from infra.repos.file.serializers import load_from_file, save_to_file

logger = logging.getLogger(__name__)


class CategoryFileRepo(CategoryRepo):
    def __init__(self, base_dir: Path = Path("data/categories")) -> None:
        self._base_dir = base_dir
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def _file_path(self, category_id: str) -> Path:
        return self._base_dir / f"{category_id}.json"

    @staticmethod
    def _from_dict(data: dict[str, Any]) -> Category:
        # Convert string fields back to proper types
        if data.get("transaction_type") is not None:
            data["transaction_type"] = TransactionType(data["transaction_type"])
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return Category(**data)

    async def create(self, category: Category) -> None:
        path = self._file_path(category.id)
        await save_to_file(path, asdict(category))
        logger.debug("Created category %s", category.id)

    async def get_by_id(self, category_id: str) -> Category | None:
        data = await load_from_file(self._file_path(category_id))
        return self._from_dict(data) if data else None

    async def get_by_user_id(self, user_id: str, transaction_type: TransactionType | None = None) -> list[Category]:
        result = []
        for path in self._base_dir.glob("*.json"):
            data = await load_from_file(path)
            if not data or data.get("user_id") != user_id:
                continue
            if transaction_type is not None and data.get("transaction_type") != transaction_type.value:
                continue
            result.append(self._from_dict(data))
        return result

    async def update(self, category: Category) -> None:
        existing = await self.get_by_id(category.id)
        if existing is None:
            raise CategoryNotFoundError(category.id)
        category.updated_at = utc_now()
        await save_to_file(self._file_path(category.id), asdict(category))
        logger.debug("Updated category %s", category.id)

    async def delete(self, category_id: str) -> None:
        path = self._file_path(category_id)
        if not path.exists():
            raise CategoryNotFoundError(category_id)
        path.unlink()
        logger.debug("Deleted category %s", category_id)
