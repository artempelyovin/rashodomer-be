from abc import ABC, abstractmethod

from domain.models.budget import Budget


class BudgetRepo(ABC):
    @abstractmethod
    async def create(self, budget: Budget) -> None: ...

    @abstractmethod
    async def get_by_id(self, budget_id: str) -> Budget | None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> list[Budget]: ...

    @abstractmethod
    async def update(self, budget: Budget) -> None: ...

    @abstractmethod
    async def delete(self, budget_id: str) -> None: ...
