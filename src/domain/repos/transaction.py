from abc import ABC, abstractmethod

from domain.models.transaction import Transaction


class TransactionRepo(ABC):
    @abstractmethod
    async def create(self, transaction: Transaction) -> None: ...

    @abstractmethod
    async def get_by_id(self, transaction_id: str) -> Transaction | None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> list[Transaction]: ...

    @abstractmethod
    async def get_by_budget_id(self, budget_id: str) -> list[Transaction]: ...

    @abstractmethod
    async def update(self, transaction: Transaction) -> None: ...

    @abstractmethod
    async def delete(self, transaction_id: str) -> None: ...
