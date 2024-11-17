# ruff: noqa: B008
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from api.base import APIResponse, APIResponseList, write_response, write_response_list
from api.budget.schemas import BudgetSchema, CreateBudgetSchema, UpdateBudgetSchema
from api.depends import authentication_user, budget_service_factory
from core.entities import User
from core.services import BudgetService
from core.use_cases.budget.create import CreateBudgetUseCase
from core.use_cases.budget.delete import DeleteBudgetUseCase
from core.use_cases.budget.find import FindBudgetUseCase
from core.use_cases.budget.get import GetBudgetUseCase
from core.use_cases.budget.list import ListBudgetUseCase
from core.use_cases.budget.update import UpdateBudgetUseCase
from core.utils import UNSET

router = APIRouter()

BUDGET_TAG = "budgets"


@router.post(
    "/v1/budgets",
    status_code=status.HTTP_201_CREATED,
    summary="Create budget",
    description="Create a new budget",
    tags=[BUDGET_TAG],
)
async def create_budget(
    body: CreateBudgetSchema,
    *,
    user: User = Depends(authentication_user),
    budget_service: BudgetService = Depends(budget_service_factory),
) -> APIResponse[BudgetSchema]:
    use_case = CreateBudgetUseCase(budget_service=budget_service)
    budget = await use_case.create(name=body.name, description=body.description, amount=body.amount, user_id=user.id)
    return write_response(result=budget, schema=BudgetSchema, status_code=status.HTTP_201_CREATED)


@router.get(
    "/v1/budgets",
    status_code=status.HTTP_200_OK,
    summary="List budget",
    description="Returns a list of the user budgets",
    tags=[BUDGET_TAG],
)
async def list_budgets(
    limit: int | None = Query(None, description="Number of budgets to return"),
    offset: int = Query(0, description="Offset of the budgets to return"),
    *,
    user: User = Depends(authentication_user),
    budget_service: BudgetService = Depends(budget_service_factory),
) -> APIResponseList[BudgetSchema]:
    use_case = ListBudgetUseCase(budget_service=budget_service)
    total, budgets = await use_case.list(user_id=user.id, limit=limit, offset=offset)
    return write_response_list(items=budgets, total=total, limit=limit, offset=offset, schema=BudgetSchema)


@router.get(
    "/v1/budgets/find",
    status_code=status.HTTP_200_OK,
    summary="Find budgets",
    description="Find budgets by name or description",
    tags=[BUDGET_TAG],
)
async def find_budgets(
    text: str = Query(..., description="Search text", example="Cash"),
    case_sensitive: bool = Query(False, description="Case sensitive when searching"),  # noqa: FBT001, FBT003
    limit: int | None = Query(None, description="Number of budgets to return"),
    offset: int = Query(0, description="Offset of the budgets to return"),
    *,
    user: User = Depends(authentication_user),
    budget_service: BudgetService = Depends(budget_service_factory),
) -> APIResponseList[BudgetSchema]:
    use_case = FindBudgetUseCase(budget_service=budget_service)
    total, budgets = await use_case.find(
        user_id=user.id, text=text, case_sensitive=case_sensitive, limit=limit, offset=offset
    )
    return write_response_list(items=budgets, total=total, limit=limit, offset=offset, schema=BudgetSchema)


@router.get(
    "/v1/budgets/{budget_id}",
    status_code=status.HTTP_200_OK,
    summary="Get budget",
    description="Returns the budget by its ID",
    tags=[BUDGET_TAG],
)
async def get_budget(
    budget_id: Annotated[str, UUID] = Path(..., description="The ID of the budget"),
    *,
    user: User = Depends(authentication_user),
    budget_service: BudgetService = Depends(budget_service_factory),
) -> APIResponse[BudgetSchema]:
    use_case = GetBudgetUseCase(budget_service=budget_service)
    budget = await use_case.get(user_id=user.id, budget_id=budget_id)
    return write_response(result=budget, schema=BudgetSchema)


@router.patch(
    "/v1/budgets/{budget_id}",
    status_code=status.HTTP_200_OK,
    summary="Update budget",
    description="Update the budget by its ID",
    tags=[BUDGET_TAG],
)
async def update_budget(
    body: UpdateBudgetSchema,
    budget_id: Annotated[str, UUID] = Path(..., description="The ID of the budget"),
    *,
    user: User = Depends(authentication_user),
    budget_service: BudgetService = Depends(budget_service_factory),
) -> APIResponse[BudgetSchema]:
    params = body.model_dump(exclude_unset=True)
    use_case = UpdateBudgetUseCase(budget_service=budget_service)
    budget = await use_case.update(
        user_id=user.id,
        budget_id=budget_id,
        name=params.get("name", UNSET),
        description=params.get("description", UNSET),
        amount=params.get("amount", UNSET),
    )
    return write_response(result=budget, schema=BudgetSchema)


@router.delete(
    "/v1/budgets/{budget_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete budget",
    description="Delete the budget by its ID",
    tags=[BUDGET_TAG],
)
async def delete_budget(
    budget_id: Annotated[str, UUID] = Path(..., description="The ID of the budget"),
    *,
    user: User = Depends(authentication_user),
    budget_service: BudgetService = Depends(budget_service_factory),
) -> APIResponse[BudgetSchema]:
    use_case = DeleteBudgetUseCase(budget_service=budget_service)
    budget = await use_case.delete(user_id=user.id, budget_id=budget_id)
    return write_response(result=budget, schema=BudgetSchema)
