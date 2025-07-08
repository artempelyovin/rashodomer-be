from pydantic import SecretStr
from pydantic_settings import BaseSettings

from repos.abc import BudgetRepo, CategoryRepo, TokenRepo, TransactionRepo, UserRepo
from repos.files import FileBudgetRepo, FileCategoryRepo, FileTokenRepo, FileTransactionRepo, FileUserRepo


class Settings(BaseSettings):
    token_repo: TokenRepo
    user_repo: UserRepo
    budget_repo: BudgetRepo
    category_repo: CategoryRepo
    transaction_repo: TransactionRepo
    storage_secret: SecretStr


settings = Settings(  # TODO: убрать тмпу hardcoded
    token_repo=FileTokenRepo(),
    user_repo=FileUserRepo(),
    budget_repo=FileBudgetRepo(),
    category_repo=FileCategoryRepo(),
    transaction_repo=FileTransactionRepo(),
    storage_secret="123456",  # TODO: изменить `storage_secret`
)
