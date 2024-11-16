# ruff: noqa: B008

from fastapi import APIRouter, Depends
from starlette import status

from api.base import APIResponse, write_response
from api.category.schemas import CategorySchema, CreateCategorySchema
from api.depends import authentication_user, category_service_factory, emoji_service_factory
from core.entities import User
from core.services import CategoryService, EmojiService
from core.use_cases.category.create import CreateCategoryUseCase

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
