# ruff: noqa: B008

from fastapi import APIRouter, Depends, Query
from starlette import status

from api.base import APIResponse, APIResponseList, write_response, write_response_list
from api.category.schemas import CategorySchema, CreateCategorySchema
from api.depends import authentication_user, category_service_factory, emoji_service_factory
from core.entities import User
from core.enums import CategoryType
from core.services import CategoryService, EmojiService
from core.use_cases.category.create import CreateCategoryUseCase
from core.use_cases.category.list import ListCategoryUseCase

router = APIRouter()


@router.post(
    "/v1/categories",
    status_code=status.HTTP_201_CREATED,
    summary="Create category",
    description="Create a new category",
    tags=["categories"],
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
        category_type=body.type,
        emoji_icon=body.emoji_icon,
    )
    return write_response(result=category, schema=CategorySchema, status_code=status.HTTP_201_CREATED)


@router.get(
    "/v1/categories",
    status_code=status.HTTP_200_OK,
    summary="List categories",
    description="Returns a list of the user categories",
    tags=["categories"],
)
async def list_categories(
    category_type: CategoryType = Query(..., description="The type of category"),
    show_archived: bool = Query(False, description="Include archived categories if `true`"),  # noqa: FBT001, FBT003
    limit: int | None = Query(None, description="Number of categories to return"),
    offset: int = Query(0, description="Offset of the categories to return"),
    *,
    user: User = Depends(authentication_user),
    category_service: CategoryService = Depends(category_service_factory),
) -> APIResponseList[CategorySchema]:
    use_case = ListCategoryUseCase(category_service=category_service)
    total, categories = await use_case.list(
        user_id=user.id, category_type=category_type, limit=limit, show_archived=show_archived, offset=offset
    )
    return write_response_list(items=categories, total=total, limit=limit, offset=offset, schema=CategorySchema)
