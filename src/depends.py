from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from managers.auth import AuthManager
from repos.abc import (
    BudgetRepo,
    CategoryRepo,
    ExpenseRepo,
    IncomeRepo,
    TokenRepo,
    UserRepo,
)
from repos.files import (
    FileBudgetRepo,
    FileCategoryRepo,
    FileExpenseRepo,
    FileIncomeRepo,
    FileTokenRepo,
    FileUserRepo,
)
from schemas.user import DetailedUserSchema

header_scheme = APIKeyHeader(
    name="Authorization", auto_error=False, description='Token in format: "Authorization": "{TOKEN}"'
)


def token_repo_factory() -> TokenRepo:
    return FileTokenRepo()


def user_repo_factory() -> UserRepo:
    return FileUserRepo()


def budget_repo_factory() -> BudgetRepo:
    return FileBudgetRepo()


def category_repo_factory() -> CategoryRepo:
    return FileCategoryRepo()


def expense_repo_factory() -> ExpenseRepo:
    return FileExpenseRepo()


def income_repo_factory() -> IncomeRepo:
    return FileIncomeRepo()


async def authentication_user(
    token: Annotated[str | None, Depends(header_scheme)],
    user_repo: Annotated[UserRepo, Depends(user_repo_factory)],
    token_repo: Annotated[TokenRepo, Depends(token_repo_factory)],
) -> DetailedUserSchema:
    manager = AuthManager(user_repo=user_repo, token_repo=token_repo)
    return await manager.authenticate(token=token)
