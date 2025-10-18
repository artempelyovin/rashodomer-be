# ruff: noqa: B008
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from base import APIResponse, APIResponseList, write_response, write_response_list
from depends import authentication_user, category_repo_factory
from enums import CategoryType
from managers.category import CategoryManager
from models.category import CategorySchema, CreateCategorySchema, UpdateCategorySchema
from models.user import DetailedUserSchema
from repos.abc import CategoryRepo
from utils import UNSET

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
    user: DetailedUserSchema = Depends(authentication_user),
    category_repo: CategoryRepo = Depends(category_repo_factory),
) -> APIResponse[CategorySchema]:
    manager = CategoryManager(category_repo=category_repo)
    category = await manager.create(user_id=user.id, data=body)
    return write_response(result=category, schema=CategorySchema, status_code=status.HTTP_201_CREATED)


@router.get(
    "/v1/categories",
    status_code=status.HTTP_200_OK,
    summary="List categories",
    description="Returns a list of the user categories",
    tags=[CATEGORY_TAG],
)
async def list_categories(
    category_type: CategoryType = Query(..., description="The type of category"),
    show_archived: bool = Query(False, description="Include archived categories if `true`"),  # noqa: FBT001, FBT003
    limit: int | None = Query(None, description="Number of categories to return"),
    offset: int = Query(0, description="Offset of the categories to return"),
    *,
    user: DetailedUserSchema = Depends(authentication_user),
    category_repo: CategoryRepo = Depends(category_repo_factory),
) -> APIResponseList[CategorySchema]:
    manager = CategoryManager(category_repo=category_repo)
    total, categories = await manager.list_(
        user_id=user.id, category_type=category_type, limit=limit, show_archived=show_archived, offset=offset
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
    user: DetailedUserSchema = Depends(authentication_user),
    category_repo: CategoryRepo = Depends(category_repo_factory),
) -> APIResponseList[CategorySchema]:
    manager = CategoryManager(category_repo=category_repo)
    total, categories = await manager.find(
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
    user: DetailedUserSchema = Depends(authentication_user),
    category_repo: CategoryRepo = Depends(category_repo_factory),
) -> APIResponse[CategorySchema]:
    manager = CategoryManager(category_repo=category_repo)
    category = await manager.get(user_id=user.id, category_id=category_id)
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
    user: DetailedUserSchema = Depends(authentication_user),
    category_repo: CategoryRepo = Depends(category_repo_factory),
) -> APIResponse[CategorySchema]:
    params = body.model_dump(exclude_unset=True)

    manager = CategoryManager(category_repo=category_repo)
    category = await manager.update(
        user_id=user.id,
        category_id=category_id,
        name=params.get("name", UNSET),
        description=params.get("description", UNSET),
        category_type=params.get("type", UNSET),
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
    user: DetailedUserSchema = Depends(authentication_user),
    category_repo: CategoryRepo = Depends(category_repo_factory),
) -> APIResponse[CategorySchema]:
    manager = CategoryManager(category_repo=category_repo)
    category = await manager.delete(user_id=user.id, category_id=category_id)
    return write_response(result=category, schema=CategorySchema)
