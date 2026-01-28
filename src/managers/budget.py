from datetime import UTC, datetime

import emoji
from pygments.lexers import data
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Budget
from db.query.budget import find_budgets_by_name, get_budget, list_budgets, count_budgets
from db.utils import fetch_all, save_and_flush, fetch_one_or_none, fetch_one
from exceptions import (
    AmountMustBePositiveError,
    BudgetAccessDeniedError,
    BudgetAlreadyExistsError,
    BudgetNotExistsError,
    EmptySearchTextError,
    NotEmojiIconError,
)
from repos.abc import Total
from schemas.budget import BudgetSchema, CreateBudgetSchema, UpdateBudgetSchema


class BudgetManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: str, data: CreateBudgetSchema) -> BudgetSchema:
        if data.amount < 0:
            raise AmountMustBePositiveError

        exist_budgets = await fetch_all(
            session=self.session, query=find_budgets_by_name(user_id=user_id, name=data.name)
        )
        if exist_budgets:
            raise BudgetAlreadyExistsError(name=data.name)
        if data.emoji_icon is not None and not emoji.is_emoji(data.emoji_icon):
            raise NotEmojiIconError(emoji_icon=data.emoji_icon)
        budget = Budget(
            name=data.name,
            description=data.description,
            amount=data.amount,
            emoji_icon=data.emoji_icon,
            user_id=user_id,
        )
        saved_budget = await save_and_flush(session=self.session, obj=budget)
        await self.session.commit()
        return BudgetSchema.model_validate(saved_budget, from_attributes=True)

    async def get(self, user_id: str, budget_id: str) -> BudgetSchema:
        budget = await fetch_one_or_none(session=self.session, query=get_budget(budget_id))
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        return BudgetSchema.model_validate(budget, from_attributes=True)

    async def list_(self, user_id: str, limit: int | None, offset: int) -> tuple[Total, list[BudgetSchema]]:
        budgets = await fetch_all(session=self.session, query=list_budgets(user_id=user_id, limit=limit, offset=offset))
        total = await fetch_one(session=self.session, query=count_budgets(user_id=user_id))
        return total, [BudgetSchema.model_validate(b, from_attributes=True) for b in budgets]

    async def update(self, user_id: str, budget_id: str, params: UpdateBudgetSchema) -> BudgetSchema:
        budget = await fetch_one_or_none(session=self.session, query=get_budget(budget_id))
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        if "amount" in params.model_fields_set and params.amount is not None and params.amount < 0:
            raise AmountMustBePositiveError

        if "name" in params.model_fields_set and params.name is not None:
            budget.name = params.name
        if "description" in params.model_fields_set and params.description is not None:
            budget.description = params.description
        if "amount" in params.model_fields_set and params.amount is not None:
            budget.amount = params.amount
        if "emoji_icon" in params.model_fields_set:
            if params.emoji_icon is not None and not emoji.is_emoji(params.emoji_icon):
                raise NotEmojiIconError(emoji_icon=params.emoji_icon)
            budget.emoji_icon = params.emoji_icon
        budget.updated_at = datetime.now(tz=UTC)
        saved_budget = await save_and_flush(session=self.session, obj=budget)
        await self.session.commit()
        return BudgetSchema.model_validate(saved_budget, from_attributes=True)

    async def delete(self, user_id: str, budget_id: str) -> BudgetSchema:
        budget = await fetch_one_or_none(session=self.session, query=get_budget(budget_id))
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        await self.session.delete(budget)
        await self.session.commit()
        return BudgetSchema.model_validate(budget, from_attributes=True)

    async def find(
        self, user_id: str, text: str, *, case_sensitive: bool, limit: int | None, offset: int
    ) -> tuple[Total, list[BudgetSchema]]:
        if len(text) == 0:
            raise EmptySearchTextError
        return await self.repo.find_by_text(
            user_id=user_id, text=text, case_sensitive=case_sensitive, limit=limit, offset=offset
        )
