from typing import Annotated

from fastapi import APIRouter, Depends, Path
from pydantic import UUID4
from starlette import status

from api.budget.schemas import BudgetListSchema, BudgetSchema, CreateBudgetSchema
from api.depends import budget_service_factory, user_service_factory
from core.services import BudgetService, UserService
from core.use_cases.create_budget import CreateBudgetUseCase
from core.use_cases.get_budget import GetBudgetUseCase
from core.use_cases.list_budgets import ListBudgetUseCase

router = APIRouter()


@router.post(
    "/v1/budgets",
    status_code=status.HTTP_201_CREATED,
    response_model=BudgetSchema,
    summary="Create budget",
    description="Create a new budget",
    tags=["budgets"],
)
async def create_budget(
    body: CreateBudgetSchema,
    user_service: Annotated[UserService, Depends(user_service_factory)],
    budget_service: Annotated[BudgetService, Depends(budget_service_factory)],
):
    use_case = CreateBudgetUseCase(user_service=user_service, budget_service=budget_service)
    return await use_case.create(name=body.name, description=body.description, amount=body.amount, user_id=body.user_id)


@router.get(
    "/v1/budgets",
    status_code=status.HTTP_200_OK,
    response_model=BudgetListSchema,
    summary="List budget",
    description="Returns a list of the user budgets",
    tags=["budgets"],
)
async def list_budgets(
    user_service: Annotated[UserService, Depends(user_service_factory)],
    budget_service: Annotated[BudgetService, Depends(budget_service_factory)],
):
    use_case = ListBudgetUseCase(user_service=user_service, budget_service=budget_service)
    return await use_case.list(user_id="2")  # TODO: get user_id from token


@router.get(
    "/v1/budgets/{budget_id}",
    status_code=status.HTTP_200_OK,
    response_model=BudgetListSchema,
    summary="Get budget",
    description="Returns the budget by its ID",
    tags=["budgets"],
)
async def list_budgets(
    user_service: Annotated[UserService, Depends(user_service_factory)],
    budget_service: Annotated[BudgetService, Depends(budget_service_factory)],
    budget_id: Annotated[str, UUID4] = Path(..., description="The ID of the budget"),
):
    use_case = GetBudgetUseCase(user_service=user_service, budget_service=budget_service)
    return await use_case.get(user_id="2", budget_id=budget_id)  # TODO: get user_id from token
