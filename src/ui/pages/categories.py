import logging
from functools import partial
from math import ceil

from nicegui import APIRouter, ui
from starlette.requests import Request

from enums import CategoryType
from managers.category import CategoryManager
from models.user import DetailedUserSchema
from ui.components.buttons import DeleteButtonWithConfirmation
from ui.components.labels import id_with_copy

logger = logging.getLogger(__name__)
router = APIRouter()


@router.page("/categories")
async def list_categories(
    request: Request,
    category_type: CategoryType = CategoryType.EXPENSE,
    show_archived: bool = False,
    page: int = 1,
    limit: int = 10,
):
    async def confirm_deletion(user_id: str, category_id: str) -> None:
        await CategoryManager().delete(user_id=user_id, category_id=category_id)
        logger.info(f"Successful delete category {category_id} for user {user_id}")
        ui.navigate.to(
            f"/categories?page=1&limit={limit}&category_type={category_type.value}&show_archived={show_archived}"
        )

    user: DetailedUserSchema = request.state.user
    logger.info(f"Show /categories page for user {user.id} with {page=}, {limit=}, {category_type=}, {show_archived=}")

    offset = (page - 1) * limit
    total, categories = await CategoryManager().list_(
        user_id=user.id,
        category_type=category_type,
        show_archived=show_archived,
        limit=limit,
        offset=offset,
    )
    logger.debug(f"Get {len(categories)} categories, {total=}")

    pages = ceil(total / limit) or 1

    with ui.row():
        ui.select(
            [CategoryType.EXPENSE, CategoryType.INCOME, CategoryType.TRANSFER],
            value=category_type,
            label="Категория",
            on_change=lambda e: ui.navigate.to(
                f"/categories?page=1&limit={limit}&category_type={e.value.value}&show_archived={show_archived}"
            ),
        )
        ui.checkbox(
            "Показать архивные",
            value=show_archived,
            on_change=lambda e: ui.navigate.to(
                f"/categories?page=1&limit={limit}&category_type={category_type.value}&show_archived={e.value}"
            ),
        )

    if len(categories) == 0:
        ui.label("У вас ещё нет категорий...")
        ui.label("Самое время создать первую категорию!")
    else:
        with ui.column():
            for category in categories:
                with ui.card():
                    with ui.row():
                        with ui.row():
                            id_with_copy(category.id)
                        with ui.row():
                            ui.button(
                                icon="edit",
                                on_click=lambda _, category_id=category.id: ui.navigate.to(
                                    f"/categories/{category_id}"
                                ),
                            )
                            DeleteButtonWithConfirmation(
                                icon="delete",
                                dialog_text=f"Вы действительно хотите удалить категорию {category.name} ({category.id})?",
                                on_delete_callback=partial(
                                    confirm_deletion,
                                    user_id=user.id,
                                    category_id=category.id,
                                ),
                            )
                    with ui.row():
                        if category.emoji_icon:
                            ui.label(category.emoji_icon).classes("text-2xl")
                        ui.label(category.name).classes("text-xl font-bold")
                        ui.badge(category.type.value, color="primary")
                        if category.is_archived:
                            ui.badge("ARCHIVED", color="negative")
                    ui.label(category.description).classes("text-sm")
                    with ui.row():
                        with ui.column():
                            ui.label("Дата создания")
                            ui.label(category.created_at).classes("text-sm")
                        with ui.column():
                            ui.label("Дата обновления")
                            ui.label(category.updated_at).classes("text-sm")

        with ui.row():
            ui.pagination(
                min=1,
                max=pages,
                value=page,
                direction_links=True,
                on_change=lambda e: ui.navigate.to(
                    f"/categories?page={e.value}&limit={limit}&category_type={category_type if category_type else ''}&show_archived={show_archived}"
                ),
            )
            ui.select(
                [5, 10, 20, 50],
                value=limit,
                on_change=lambda e: ui.navigate.to(
                    f"/categories?page=1&limit={e.value}&category_type={category_type if category_type else ''}&show_archived={show_archived}"
                ),
            )

    with ui.page_sticky(x_offset=18, y_offset=18):
        ui.button("+", on_click=lambda: ui.navigate.to("/categories/new")).props("fab")


@router.page("/categories/new")
async def create_category(request: Request):
    user: DetailedUserSchema = request.state.user

    async def validate_and_create(
        name: str, description: str, category_type: CategoryType, emoji_icon: str | None
    ) -> None:
        if not name:
            return ui.notify("Заполните название", type="negative")
        await CategoryManager().create(
            user_id=user.id, name=name, description=description, category_type=category_type, emoji_icon=emoji_icon
        )
        ui.navigate.to("/categories")

    with ui.row():
        ui.button(icon="arrow_back", on_click=ui.navigate.back)
        ui.label("Создание новой категории")

    name = ui.input("Название*")
    description = ui.textarea("Описание")
    category_type = ui.select(
        [CategoryType.EXPENSE, CategoryType.INCOME, CategoryType.TRANSFER],
        value=CategoryType.EXPENSE,
        label="Категория*",
    )
    emoji_icon = ui.input("Emoji иконка").classes("text-2xl")

    ui.button(
        "Создать",
        on_click=lambda _: validate_and_create(
            name=name.value,
            description=description.value,
            category_type=category_type.value,
            emoji_icon=emoji_icon.value if emoji_icon.value else None,
        ),
    )


@router.page("/categories/{category_id}")
async def update_category(request: Request, category_id: str):
    user: DetailedUserSchema = request.state.user
    logger.info(f"Show /categories/{category_id} page for user {user.id}")

    category = await CategoryManager().get(user_id=user.id, category_id=category_id)

    async def validate_and_save(
        name: str, description: str, category_type: CategoryType, is_archived: bool, emoji_icon: str | None
    ) -> None:
        if not name:
            return ui.notify("Заполните название", type="negative")
        await CategoryManager().update(
            user_id=user.id,
            category_id=category.id,
            name=name,
            description=description,
            category_type=category_type,
            is_archived=is_archived,
            emoji_icon=emoji_icon,
        )
        ui.navigate.to("/categories")

    with ui.row():
        ui.button(icon="arrow_back", on_click=ui.navigate.back)
        ui.label("Редактирование категории")

    name = ui.input("Название", value=category.name)
    description = ui.textarea("Описание", value=category.description)
    category_type = ui.select(
        [CategoryType.EXPENSE, CategoryType.INCOME, CategoryType.TRANSFER],
        value=category.type,
        label="Тип категории",
    )
    is_archived = ui.checkbox("Архивировано", value=category.is_archived)
    emoji_icon = ui.input("Emoji иконка", value=category.emoji_icon or "").classes("text-2xl")

    ui.button(
        "Сохранить",
        on_click=lambda _: validate_and_save(
            name=name.value,
            description=description.value,
            category_type=category_type.value,
            is_archived=is_archived.value,
            emoji_icon=emoji_icon.value if emoji_icon.value else None,
        ),
    )
