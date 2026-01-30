from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from base import ListSchema, write_response_list
from depends import authentication_user, get_async_session
from managers.budget import BudgetManager
from schemas.budget import BudgetSchema, CreateBudgetSchema, UpdateBudgetSchema
from schemas.user import DetailedUserSchema
from utils import UUID4Str

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
    session: AsyncSession = Depends(get_async_session),
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
) -> BudgetSchema:
    manager = BudgetManager(session=session)
    return await manager.create(user_id=user.id, data=body)


@router.get(
    "/v1/budgets",
    status_code=status.HTTP_200_OK,
    summary="List budget",
    description="Returns a list of the user budgets",
    tags=[BUDGET_TAG],
)
async def list_budgets(
    limit: Annotated[int | None, Query(description="Number of budgets to return")] = None,
    offset: Annotated[int, Query(description="Offset of the budgets to return")] = 0,
    *,
    session: AsyncSession = Depends(get_async_session),
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
) -> ListSchema[BudgetSchema]:
    manager = BudgetManager(session=session)
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
    text: Annotated[str, Query(description="Search text", examples=["Cash"])],
    case_sensitive: Annotated[bool, Query(description="Case sensitive when searching")] = False,  # noqa: FBT002
    limit: Annotated[int | None, Query(description="Number of budgets to return")] = None,
    offset: Annotated[int, Query(description="Offset of the budgets to return")] = 0,
    *,
    session: AsyncSession = Depends(get_async_session),
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
) -> ListSchema[BudgetSchema]:
    manager = BudgetManager(session=session)
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
    budget_id: Annotated[Annotated[str, UUID4Str], Path(description="The ID of the budget")],
    *,
    session: AsyncSession = Depends(get_async_session),
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
) -> BudgetSchema:
    manager = BudgetManager(session=session)
    return await manager.get(user_id=user.id, budget_id=budget_id)


@router.patch(
    "/v1/budgets/{budget_id}",
    status_code=status.HTTP_200_OK,
    summary="Update budget",
    description="Update the budget by its ID",
    tags=[BUDGET_TAG],
)
async def update_budget(
    body: UpdateBudgetSchema,
    budget_id: Annotated[Annotated[str, UUID4Str], Path(description="The ID of the budget")],
    *,
    session: AsyncSession = Depends(get_async_session),
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
) -> BudgetSchema:
    manager = BudgetManager(session=session)
    return await manager.update(user_id=user.id, budget_id=budget_id, params=body)


@router.delete(
    "/v1/budgets/{budget_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete budget",
    description="Delete the budget by its ID",
    tags=[BUDGET_TAG],
)
async def delete_budget(
    budget_id: Annotated[Annotated[str, UUID4Str], Path(description="The ID of the budget")],
    *,
    session: AsyncSession = Depends(get_async_session),
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
) -> BudgetSchema:
    manager = BudgetManager(session=session)
    return await manager.delete(user_id=user.id, budget_id=budget_id)
