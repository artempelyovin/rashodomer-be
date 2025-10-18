# ruff: noqa: B008
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from base import APIResponse, APIResponseList, write_response, write_response_list
from depends import authentication_user, category_repo_factory, transaction_repo_factory
from managers.transaction import TransactionManager
from repos.abc import CategoryRepo, TransactionRepo
from schemas.transaction import CreateTransactionSchema, TransactionSchema, UpdateTransactionSchema
from schemas.user import DetailedUserSchema
from utils import UNSET

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
    user: DetailedUserSchema = Depends(authentication_user),
    transaction_repo: TransactionRepo = Depends(transaction_repo_factory),
    category_repo: CategoryRepo = Depends(category_repo_factory),
) -> APIResponse[TransactionSchema]:
    manager = TransactionManager(transaction_repo=transaction_repo, category_repo=category_repo)
    transaction = await manager.create(user_id=user.id, data=body)
    return write_response(result=transaction, schema=TransactionSchema, status_code=status.HTTP_201_CREATED)


@router.get(
    "/v1/transactions",
    status_code=status.HTTP_200_OK,
    summary="List transactions",
    description="Returns a list of the user transactions",
    tags=[TRANSACTION_TAG],
)
async def list_transactions(
    limit: int | None = Query(None, description="Number of transactions to return"),
    offset: int = Query(0, description="Offset of the transactions to return"),
    *,
    user: DetailedUserSchema = Depends(authentication_user),
    transaction_repo: TransactionRepo = Depends(transaction_repo_factory),
    category_repo: CategoryRepo = Depends(category_repo_factory),
) -> APIResponseList[TransactionSchema]:
    manager = TransactionManager(transaction_repo=transaction_repo, category_repo=category_repo)
    total, transactions = await manager.list_(user_id=user.id, limit=limit, offset=offset)
    return write_response_list(items=transactions, total=total, limit=limit, offset=offset, schema=TransactionSchema)


@router.get(
    "/v1/transactions/find",
    status_code=status.HTTP_200_OK,
    summary="Find transactions",
    description="Find transactions by name or description",
    tags=[TRANSACTION_TAG],
)
async def find_transactions(
    text: str = Query(..., description="Search text", example="Cash"),
    case_sensitive: bool = Query(False, description="Case sensitive when searching"),  # noqa: FBT001, FBT003
    limit: int | None = Query(None, description="Number of transactions to return"),
    offset: int = Query(0, description="Offset of the transactions to return"),
    *,
    user: DetailedUserSchema = Depends(authentication_user),
    transaction_repo: TransactionRepo = Depends(transaction_repo_factory),
    category_repo: CategoryRepo = Depends(category_repo_factory),
) -> APIResponseList[TransactionSchema]:
    manager = TransactionManager(transaction_repo=transaction_repo, category_repo=category_repo)
    total, transactions = await manager.find(
        user_id=user.id, text=text, case_sensitive=case_sensitive, limit=limit, offset=offset
    )
    return write_response_list(items=transactions, total=total, limit=limit, offset=offset, schema=TransactionSchema)


@router.get(
    "/v1/transactions/{transaction_id}",
    status_code=status.HTTP_200_OK,
    summary="Get transaction",
    description="Returns the transaction by its ID",
    tags=[TRANSACTION_TAG],
)
async def get_transaction(
    transaction_id: Annotated[str, UUID] = Path(..., description="The ID of the transaction"),
    *,
    user: DetailedUserSchema = Depends(authentication_user),
    transaction_repo: TransactionRepo = Depends(transaction_repo_factory),
    category_repo: CategoryRepo = Depends(category_repo_factory),
) -> APIResponse[TransactionSchema]:
    manager = TransactionManager(transaction_repo=transaction_repo, category_repo=category_repo)
    transaction = await manager.get(user_id=user.id, transaction_id=transaction_id)
    return write_response(result=transaction, schema=TransactionSchema)


@router.patch(
    "/v1/transactions/{transaction_id}",
    status_code=status.HTTP_200_OK,
    summary="Update transaction",
    description="Update the transaction by its ID",
    tags=[TRANSACTION_TAG],
)
async def update_transaction(
    body: UpdateTransactionSchema,
    transaction_id: Annotated[str, UUID] = Path(..., description="The ID of the transaction"),
    *,
    user: DetailedUserSchema = Depends(authentication_user),
    transaction_repo: TransactionRepo = Depends(transaction_repo_factory),
    category_repo: CategoryRepo = Depends(category_repo_factory),
) -> APIResponse[TransactionSchema]:
    params = body.model_dump(exclude_unset=True)

    manager = TransactionManager(transaction_repo=transaction_repo, category_repo=category_repo)
    transaction = await manager.update(
        user_id=user.id,
        transaction_id=transaction_id,
        amount=params.get("amount", UNSET),
        description=params.get("description", UNSET),
        category_id=params.get("category_id", UNSET),
        timestamp=params.get("timestamp", UNSET),
    )
    return write_response(result=transaction, schema=TransactionSchema)


@router.delete(
    "/v1/transactions/{transaction_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete transaction",
    description="Delete the transaction by its ID",
    tags=[TRANSACTION_TAG],
)
async def delete_transaction(
    transaction_id: Annotated[str, UUID] = Path(..., description="The ID of the transaction"),
    *,
    user: DetailedUserSchema = Depends(authentication_user),
    transaction_repo: TransactionRepo = Depends(transaction_repo_factory),
    category_repo: CategoryRepo = Depends(category_repo_factory),
) -> APIResponse[TransactionSchema]:
    manager = TransactionManager(transaction_repo=transaction_repo, category_repo=category_repo)
    transaction = await manager.delete(user_id=user.id, transaction_id=transaction_id)
    return write_response(result=transaction, schema=TransactionSchema)
