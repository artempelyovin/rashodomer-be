import logging
from dataclasses import asdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from domain.errors import BudgetNotFoundError
from domain.models.budget import Budget
from domain.repos.budget import BudgetRepo
from domain.utils import utc_now
from infra.repos.file.serializers import load_from_file, save_to_file

logger = logging.getLogger(__name__)


class BudgetFileRepo(BudgetRepo):
    def __init__(self, base_dir: Path = Path("data/budgets")) -> None:
        self._base_dir = base_dir
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def _file_path(self, budget_id: str) -> Path:
        return self._base_dir / f"{budget_id}.json"

    @staticmethod
    def _from_dict(data: dict[str, Any]) -> Budget:
        # Convert string fields back to proper types
        data["balance"] = Decimal(data["balance"])
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return Budget(**data)

    async def create(self, budget: Budget) -> None:
        path = self._file_path(budget.id)
        await save_to_file(path, asdict(budget))
        logger.debug("Created budget %s", budget.id)

    async def get_by_id(self, budget_id: str) -> Budget | None:
        data = await load_from_file(self._file_path(budget_id))
        if data is None:
            return None
        return self._from_dict(data)

    async def get_by_user_id(self, user_id: str) -> list[Budget]:
        budgets = []
        for path in self._base_dir.glob("*.json"):
            data = await load_from_file(path)
            if data and data.get("user_id") == user_id:
                budgets.append(self._from_dict(data))
        return budgets

    async def update(self, budget: Budget) -> None:
        existing = await self.get_by_id(budget.id)
        if existing is None:
            raise BudgetNotFoundError(budget_id=budget.id)
        budget.updated_at = utc_now()
        await save_to_file(self._file_path(budget.id), asdict(budget))
        logger.debug("Updated budget %s", budget.id)

    async def delete(self, budget_id: str) -> None:
        path = self._file_path(budget_id)
        if not path.exists():
            raise BudgetNotFoundError(budget_id=budget_id)
        path.unlink()
        logger.debug("Deleted budget %s", budget_id)
