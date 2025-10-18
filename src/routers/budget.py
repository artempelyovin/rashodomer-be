# ruff: noqa: B008
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from base import APIResponse, APIResponseList, write_response, write_response_list
from depends import authentication_user, budget_repo_factory
from managers.budget import BudgetManager
from repos.abc import BudgetRepo
from schemas.budget import BudgetSchema, CreateBudgetSchema, UpdateBudgetSchema
from schemas.user import DetailedUserSchema
from utils import UNSET

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
    user: DetailedUserSchema = Depends(authentication_user),
    budget_repo: BudgetRepo = Depends(budget_repo_factory),
) -> APIResponse[BudgetSchema]:
    manager = BudgetManager(budget_repo=budget_repo)
    budget = await manager.create(user_id=user.id, data=body)
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
    user: DetailedUserSchema = Depends(authentication_user),
    budget_repo: BudgetRepo = Depends(budget_repo_factory),
) -> APIResponseList[BudgetSchema]:
    manager = BudgetManager(budget_repo=budget_repo)
    total, budgets = await manager.list_(user_id=user.id, limit=limit, offset=offset)
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
    user: DetailedUserSchema = Depends(authentication_user),
    budget_repo: BudgetRepo = Depends(budget_repo_factory),
) -> APIResponseList[BudgetSchema]:
    manager = BudgetManager(budget_repo=budget_repo)
    total, budgets = await manager.find(
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
    user: DetailedUserSchema = Depends(authentication_user),
    budget_repo: BudgetRepo = Depends(budget_repo_factory),
) -> APIResponse[BudgetSchema]:
    manager = BudgetManager(budget_repo=budget_repo)
    budget = await manager.get(user_id=user.id, budget_id=budget_id)
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
    user: DetailedUserSchema = Depends(authentication_user),
    budget_repo: BudgetRepo = Depends(budget_repo_factory),
) -> APIResponse[BudgetSchema]:
    params = body.model_dump(exclude_unset=True)
    manager = BudgetManager(budget_repo=budget_repo)
    budget = await manager.update(
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
    user: DetailedUserSchema = Depends(authentication_user),
    budget_repo: BudgetRepo = Depends(budget_repo_factory),
) -> APIResponse[BudgetSchema]:
    manager = BudgetManager(budget_repo=budget_repo)
    budget = await manager.delete(user_id=user.id, budget_id=budget_id)
    return write_response(result=budget, schema=BudgetSchema)
