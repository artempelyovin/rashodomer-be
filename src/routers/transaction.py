from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from base import ListSchema, write_response_list
from depends import authentication_user, category_repo_factory, transaction_repo_factory
from managers.transaction import TransactionManager
from repos.abc import CategoryRepo, TransactionRepo
from schemas.transaction import CreateTransactionSchema, TransactionSchema, UpdateTransactionSchema
from schemas.user import DetailedUserSchema

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
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
    transaction_repo: Annotated[TransactionRepo, Depends(transaction_repo_factory)],
    category_repo: Annotated[CategoryRepo, Depends(category_repo_factory)],
) -> TransactionSchema:
    manager = TransactionManager(transaction_repo=transaction_repo, category_repo=category_repo)
    return await manager.create(user_id=user.id, data=body)


@router.get(
    "/v1/transactions",
    status_code=status.HTTP_200_OK,
    summary="List transactions",
    description="Returns a list of the user transactions",
    tags=[TRANSACTION_TAG],
)
async def list_transactions(
    limit: Annotated[int | None, Query(description="Number of transactions to return")] = None,
    offset: Annotated[int, Query(description="Offset of the transactions to return")] = 0,
    *,
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
    transaction_repo: Annotated[TransactionRepo, Depends(transaction_repo_factory)],
    category_repo: Annotated[CategoryRepo, Depends(category_repo_factory)],
) -> ListSchema[TransactionSchema]:
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
    text: Annotated[str, Query(description="Search text", examples=["Buy a car"])],
    case_sensitive: Annotated[bool, Query(description="Case sensitive when searching")] = False,  # noqa: FBT002
    limit: Annotated[int | None, Query(description="Number of transactions to return")] = None,
    offset: Annotated[int, Query(description="Offset of the transactions to return")] = 0,
    *,
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
    transaction_repo: Annotated[TransactionRepo, Depends(transaction_repo_factory)],
    category_repo: Annotated[CategoryRepo, Depends(category_repo_factory)],
) -> ListSchema[TransactionSchema]:
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
    transaction_id: Annotated[Annotated[str, UUID], Path(description="The ID of the transaction")],
    *,
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
    transaction_repo: Annotated[TransactionRepo, Depends(transaction_repo_factory)],
    category_repo: Annotated[CategoryRepo, Depends(category_repo_factory)],
) -> TransactionSchema:
    manager = TransactionManager(transaction_repo=transaction_repo, category_repo=category_repo)
    return await manager.get(user_id=user.id, transaction_id=transaction_id)


@router.patch(
    "/v1/transactions/{transaction_id}",
    status_code=status.HTTP_200_OK,
    summary="Update transaction",
    description="Update the transaction by its ID",
    tags=[TRANSACTION_TAG],
)
async def update_transaction(
    body: UpdateTransactionSchema,
    transaction_id: Annotated[Annotated[str, UUID], Path(description="The ID of the transaction")],
    *,
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
    transaction_repo: Annotated[TransactionRepo, Depends(transaction_repo_factory)],
    category_repo: Annotated[CategoryRepo, Depends(category_repo_factory)],
) -> TransactionSchema:
    manager = TransactionManager(transaction_repo=transaction_repo, category_repo=category_repo)
    return await manager.update(user_id=user.id, transaction_id=transaction_id, params=body)


@router.delete(
    "/v1/transactions/{transaction_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete transaction",
    description="Delete the transaction by its ID",
    tags=[TRANSACTION_TAG],
)
async def delete_transaction(
    transaction_id: Annotated[Annotated[str, UUID], Path(description="The ID of the transaction")],
    *,
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
    transaction_repo: Annotated[TransactionRepo, Depends(transaction_repo_factory)],
    category_repo: Annotated[CategoryRepo, Depends(category_repo_factory)],
) -> TransactionSchema:
    manager = TransactionManager(transaction_repo=transaction_repo, category_repo=category_repo)
    return await manager.delete(user_id=user.id, transaction_id=transaction_id)
