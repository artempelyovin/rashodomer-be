# ruff: noqa: B008
from fastapi import APIRouter, Depends
from starlette import status

from api.base import APIResponse, write_response
from api.depends import (
    authentication_user,
    budget_service_factory,
    category_service_factory,
    transaction_service_factory,
)
from api.transaction.schemas import CreateTransactionSchema, TransactionSchema
from core.entities import User
from core.repos import BudgetRepository, CategoryRepository, TransactionRepository
from core.use_cases.transaction.create import CreateTransactionUseCase

router = APIRouter()

TRANSACTION_TAG = "transactions"


@router.post(
    "/v1/transactions",
    status_code=status.HTTP_201_CREATED,
    summary="Create transaction",
    description="Create a new transaction",
    tags=[TRANSACTION_TAG],
)
async def create_transaction(
    body: CreateTransactionSchema,
    *,
    user: User = Depends(authentication_user),
    budget_service: BudgetRepository = Depends(budget_service_factory),
    category_service: CategoryRepository = Depends(category_service_factory),
    transaction_service: TransactionRepository = Depends(transaction_service_factory),
) -> APIResponse[TransactionSchema]:
    use_case = CreateTransactionUseCase(
        budget_service=budget_service, category_service=category_service, transaction_service=transaction_service
    )
    category = await use_case.create(
        user_id=user.id,
        amount=body.amount,
        description=body.description,
        transaction_type=body.type,
        budget_id=body.budget_id,
        category_id=body.category_id,
        timestamp=body.timestamp,
    )
    return write_response(result=category, schema=TransactionSchema, status_code=status.HTTP_201_CREATED)
