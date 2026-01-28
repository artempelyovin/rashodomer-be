from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from base import ListSchema, write_response_list
from depends import authentication_user, category_repo_factory
from enums import CategoryType
from managers.category import CategoryManager
from repos.abc import CategoryRepo
from schemas.category import CategorySchema, CreateCategorySchema, UpdateCategorySchema
from schemas.user import DetailedUserSchema
from utils import UUID4Str

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
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
    category_repo: Annotated[CategoryRepo, Depends(category_repo_factory)],
) -> CategorySchema:
    manager = CategoryManager(category_repo=category_repo)
    return await manager.create(user_id=user.id, data=body)


@router.get(
    "/v1/categories",
    status_code=status.HTTP_200_OK,
    summary="List categories",
    description="Returns a list of the user categories",
    tags=[CATEGORY_TAG],
)
async def list_categories(
    category_type: Annotated[CategoryType, Query(description="The type of category")],
    show_archived: Annotated[bool, Query(description="Include archived categories if `true`")] = False,  # noqa: FBT002
    limit: Annotated[int | None, Query(description="Number of categories to return")] = None,
    offset: Annotated[int, Query(description="Offset of the categories to return")] = 0,
    *,
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
    category_repo: Annotated[CategoryRepo, Depends(category_repo_factory)],
) -> ListSchema[CategorySchema]:
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
    text: Annotated[str, Query(description="Search text", example=["Food"])],
    case_sensitive: Annotated[bool, Query(description="Case sensitive when searching")] = False,  # noqa: FBT002
    limit: Annotated[int | None, Query(description="Number of categories to return")] = None,
    offset: Annotated[int, Query(description="Offset of the categories to return")] = 0,
    *,
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
    category_repo: Annotated[CategoryRepo, Depends(category_repo_factory)],
) -> ListSchema[CategorySchema]:
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
    category_id: Annotated[Annotated[str, UUID4Str], Path(description="The ID of the category")],
    *,
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
    category_repo: Annotated[CategoryRepo, Depends(category_repo_factory)],
) -> CategorySchema:
    manager = CategoryManager(category_repo=category_repo)
    return await manager.get(user_id=user.id, category_id=category_id)


@router.patch(
    "/v1/categories/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Update category",
    description="Update the category by its ID",
    tags=[CATEGORY_TAG],
)
async def update_category(
    body: UpdateCategorySchema,
    category_id: Annotated[Annotated[str, UUID4Str], Path(description="The ID of the category")],
    *,
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
    category_repo: Annotated[CategoryRepo, Depends(category_repo_factory)],
) -> CategorySchema:
    manager = CategoryManager(category_repo=category_repo)
    return await manager.update(user_id=user.id, category_id=category_id, params=body)


@router.delete(
    "/v1/categories/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete category",
    description="Delete the category by its ID",
    tags=[CATEGORY_TAG],
)
async def delete_categories(
    category_id: Annotated[Annotated[str, UUID4Str], Path(description="The ID of the category")],
    *,
    user: Annotated[DetailedUserSchema, Depends(authentication_user)],
    category_repo: Annotated[CategoryRepo, Depends(category_repo_factory)],
) -> CategorySchema:
    manager = CategoryManager(category_repo=category_repo)
    return await manager.delete(user_id=user.id, category_id=category_id)
