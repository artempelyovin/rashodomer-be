from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.budget.schemas import BudgetSchema, CreateBudgetSchema
from api.depends import budget_service_factory, user_service_factory
from core.services import BudgetService, UserService
from core.use_cases.create_budget import CreateBudgetUseCase

router = APIRouter()


@router.post(
    "/v1/budgets",
    status_code=status.HTTP_201_CREATED,
    response_model=BudgetSchema,
    summary="Create budget",
    description="Create a new budget",
    tags=["budgets"],
)
async def register(
    body: CreateBudgetSchema,
    user_service: Annotated[UserService, Depends(user_service_factory)],
    budget_service: Annotated[BudgetService, Depends(budget_service_factory)],
):
    use_case = CreateBudgetUseCase(user_service=user_service, budget_service=budget_service)
    return await use_case.create(name=body.name, description=body.description, amount=body.amount, user_id=body.user_id)
