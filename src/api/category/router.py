# ruff: noqa: B008
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from api.base import APIResponse, APIResponseList, write_response, write_response_list
from api.category.schemas import CategorySchema, CreateCategorySchema, UpdateCategorySchema
from api.depends import authentication_user, category_service_factory, emoji_service_factory
from core.entities import User
from core.enums import TransactionType
from core.services import CategoryService, EmojiService
from core.use_cases.category.create import CreateCategoryUseCase
from core.use_cases.category.delete import DeleteCategoryUseCase
from core.use_cases.category.find import FindCategoryUseCase
from core.use_cases.category.get import GetCategoryUseCase
from core.use_cases.category.list import ListCategoryUseCase
from core.use_cases.category.update import UpdateCategoryUseCase
from core.utils import UNSET

router = APIRouter()

CATEGORY_TAG = "categories"


@router.post(
    "/v1/categories",
    status_code=status.HTTP_201_CREATED,
    summary="Create category",
    description="Create a new category",
    tags=[CATEGORY_TAG],
)
async def create_category(
    body: CreateCategorySchema,
    *,
    user: User = Depends(authentication_user),
    category_service: CategoryService = Depends(category_service_factory),
    emoji_service: EmojiService = Depends(emoji_service_factory),
) -> APIResponse[CategorySchema]:
    use_case = CreateCategoryUseCase(category_service=category_service, emoji_service=emoji_service)
    category = await use_case.create(
        user_id=user.id,
        name=body.name,
        description=body.description,
        transaction_type=body.type,
        emoji_icon=body.emoji_icon,
    )
    return write_response(result=category, schema=CategorySchema, status_code=status.HTTP_201_CREATED)


@router.get(
    "/v1/categories",
    status_code=status.HTTP_200_OK,
    summary="List categories",
    description="Returns a list of the user categories",
    tags=[CATEGORY_TAG],
)
async def list_categories(
    transaction_type: TransactionType = Query(..., description="The category transaction type"),
    show_archived: bool = Query(False, description="Include archived categories if `true`"),  # noqa: FBT001, FBT003
    limit: int | None = Query(None, description="Number of categories to return"),
    offset: int = Query(0, description="Offset of the categories to return"),
    *,
    user: User = Depends(authentication_user),
    category_service: CategoryService = Depends(category_service_factory),
) -> APIResponseList[CategorySchema]:
    use_case = ListCategoryUseCase(category_service=category_service)
    total, categories = await use_case.list(
        user_id=user.id, transaction_type=transaction_type, limit=limit, show_archived=show_archived, offset=offset
    )
    return write_response_list(items=categories, total=total, limit=limit, offset=offset, schema=CategorySchema)


@router.get(
    "/v1/categories/find",
    status_code=status.HTTP_200_OK,
    summary="Find categories",
    description="Find categories by name or description",
    tags=[CATEGORY_TAG],
)
async def find_categories(
    text: str = Query(..., description="Search text", example="Cash"),
    case_sensitive: bool = Query(False, description="Case sensitive when searching"),  # noqa: FBT001, FBT003
    limit: int | None = Query(None, description="Number of categories to return"),
    offset: int = Query(0, description="Offset of the categories to return"),
    *,
    user: User = Depends(authentication_user),
    category_service: CategoryService = Depends(category_service_factory),
) -> APIResponseList[CategorySchema]:
    use_case = FindCategoryUseCase(category_service=category_service)
    total, categories = await use_case.find(
        user_id=user.id, text=text, case_sensitive=case_sensitive, limit=limit, offset=offset
    )
    return write_response_list(items=categories, total=total, limit=limit, offset=offset, schema=CategorySchema)


@router.get(
    "/v1/categories/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Get category",
    description="Returns the category by its ID",
    tags=[CATEGORY_TAG],
)
async def get_category(
    category_id: Annotated[str, UUID] = Path(..., description="The ID of the category"),
    *,
    user: User = Depends(authentication_user),
    category_service: CategoryService = Depends(category_service_factory),
) -> APIResponse[CategorySchema]:
    use_case = GetCategoryUseCase(category_service=category_service)
    category = await use_case.get(user_id=user.id, category_id=category_id)
    return write_response(result=category, schema=CategorySchema)


@router.patch(
    "/v1/categories/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Update category",
    description="Update the category by its ID",
    tags=[CATEGORY_TAG],
)
async def update_category(
    body: UpdateCategorySchema,
    category_id: Annotated[str, UUID] = Path(..., description="The ID of the category"),
    *,
    user: User = Depends(authentication_user),
    category_service: CategoryService = Depends(category_service_factory),
) -> APIResponse[CategorySchema]:
    params = body.model_dump(exclude_unset=True)
    use_case = UpdateCategoryUseCase(category_service=category_service)
    category = await use_case.update(
        user_id=user.id,
        category_id=category_id,
        name=params.get("name", UNSET),
        description=params.get("description", UNSET),
        transaction_type=params.get("type", UNSET),
        is_archived=params.get("is_archived", UNSET),
        emoji_icon=params.get("emoji_icon", UNSET),
    )
    return write_response(result=category, schema=CategorySchema)


@router.delete(
    "/v1/categories/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete category",
    description="Delete the category by its ID",
    tags=[CATEGORY_TAG],
)
async def delete_categories(
    category_id: Annotated[str, UUID] = Path(..., description="The ID of the category"),
    *,
    user: User = Depends(authentication_user),
    category_service: CategoryService = Depends(category_service_factory),
) -> APIResponse[CategorySchema]:
    use_case = DeleteCategoryUseCase(category_service=category_service)
    category = await use_case.delete(user_id=user.id, category_id=category_id)
    return write_response(result=category, schema=CategorySchema)
