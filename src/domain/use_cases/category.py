import logging

from domain.errors import CategoryNotFoundError, EmptyNameError
from domain.models.category import Category
from domain.models.transaction import TransactionType
from domain.repos.category import CategoryRepo
from domain.utils import UNSET, Unset, uuid4_str

logger = logging.getLogger(__name__)


class CreateCategory:
    def __init__(self, repo: CategoryRepo) -> None:
        self._repo = repo

    async def execute(
        self, name: str, user_id: str, transaction_type: TransactionType | None = None, description: str | None = None
    ) -> Category:
        if not name or not name.strip():
            raise EmptyNameError(field="name")

        category_id = uuid4_str()
        category = Category(
            id=category_id,
            name=name,
            user_id=user_id,
            transaction_type=transaction_type,
            description=description,
        )
        await self._repo.create(category)
        logger.info("Created category %s for user %s", category_id, user_id)
        return category


class GetCategory:
    def __init__(self, repo: CategoryRepo) -> None:
        self._repo = repo

    async def execute(self, category_id: str) -> Category:
        category = await self._repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(category_id)
        logger.info("Retrieved category %s", category_id)
        return category


class ListCategories:
    def __init__(self, repo: CategoryRepo) -> None:
        self._repo = repo

    async def execute(self, user_id: str, transaction_type: TransactionType | None = None) -> list[Category]:
        categories = await self._repo.get_by_user_id(user_id, transaction_type)
        logger.info("Listed %d categories for user %s", len(categories), user_id)
        return categories


class UpdateCategory:
    def __init__(self, repo: CategoryRepo) -> None:
        self._repo = repo

    async def execute(
        self,
        category_id: str,
        name: str | Unset = UNSET,
        transaction_type: TransactionType | None | Unset = UNSET,
        description: str | None | Unset = UNSET,
    ) -> Category:
        category = await self._repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(category_id)

        if not isinstance(name, Unset):
            if not name.strip():
                raise EmptyNameError(field="name")
            category.name = name

        if not isinstance(transaction_type, Unset):
            category.transaction_type = transaction_type

        if not isinstance(description, Unset):
            category.description = description

        await self._repo.update(category)
        logger.info("Updated category %s", category_id)
        return category


class DeleteCategory:
    def __init__(self, repo: CategoryRepo) -> None:
        self._repo = repo

    async def execute(self, category_id: str) -> None:
        existing = await self._repo.get_by_id(category_id)
        if existing is None:
            raise CategoryNotFoundError(category_id)
        await self._repo.delete(category_id)
        logger.info("Deleted category %s", category_id)
