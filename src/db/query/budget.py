from sqlalchemy import select, Select, Delete, delete, Update, func

from db.models import Budget


def get_budget(budget_id: str) -> Select[tuple[Budget]]:
    return select(Budget).where(Budget.id == budget_id)


def list_budgets(user_id: str, limit: int | None = None, offset: int = 0) -> Select[tuple[Budget]]:
    return select(Budget).where(Budget.user_id == user_id).limit(limit).offset(offset)


def count_budgets(user_id: str) -> Select[tuple[int]]:
    return select(func.count()).select_from(Budget).where(Budget.user_id == user_id)


def find_budgets_by_name(user_id: str, name: str, limit: int | None = None, offset: int = 0):
    # TODO: более умный поиск
    return select(Budget).where(Budget.user_id == user_id).where(Budget.name == name).limit(limit).offset(offset)


def find_budgets_by_text(
    user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
):
    # TODO: более умный поиск
    # TODO: учесть case_sensitive
    return select(Budget).where(Budget.user_id == user_id).where(Budget.description == text).limit(limit).offset(offset)


def update_budget() -> Update:
    # TODO: написать
    pass


def delete_budget(budget_id: str) -> Delete:
    return delete(Budget).where(Budget.id == budget_id)
