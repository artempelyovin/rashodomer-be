import logging
from datetime import UTC, datetime, timezone
from functools import partial
from math import ceil

from nicegui import APIRouter, ui
from starlette.requests import Request

from managers.category import CategoryManager
from managers.transaction import TransactionManager
from models import CategorySchema, DetailedUserSchema
from ui.components.buttons import DatePickerButton, DeleteButtonWithConfirmation, TimePickerButton
from ui.components.labels import amount_with_gradient, id_with_copy

logger = logging.getLogger(__name__)
router = APIRouter()


@router.page("/transactions")
async def list_transactions(request: Request, page: int = 1, limit: int = 10, search_text: str = ""):
    async def confirm_deletion(user_id: str, transaction_id: str) -> None:
        await TransactionManager().delete(user_id=user_id, transaction_id=transaction_id)
        logger.info(f"Successful delete transaction {transaction_id} for user {user_id}")
        ui.navigate.to(f"/transactions?page={page}&limit={limit}&search_text={search_text}")

    user: DetailedUserSchema = request.state.user
    logger.info(f"Show /transactions page for user {user.id} with {page=}, {limit=}, {search_text=}")

    offset = (page - 1) * limit
    if search_text:
        total, transactions = await TransactionManager().find(
            user_id=user.id, text=search_text, case_sensitive=False, limit=limit, offset=offset
        )
    else:
        total, transactions = await TransactionManager().list_(user_id=user.id, limit=limit, offset=offset)
    logger.debug(f"Get {len(transactions)} transactions, {total=}")

    pages = ceil(total / limit) or 1

    with ui.row().classes("w-full"):
        ui.input(
            value=search_text,
            on_change=lambda e: ui.navigate.to(f"/transactions?page=1&limit={limit}&search_text={e.value}"),
            placeholder="Поиск по описанию",
        ).classes("w-full")

    if len(transactions) == 0:
        ui.label("У вас ещё нет транзакций...")
        ui.label("Самое время создать первую транзакцию!")
    else:
        with ui.column():
            for transaction in transactions:
                category = await CategoryManager().get(user_id=user.id, category_id=transaction.category_id)
                with ui.card():
                    with ui.row():
                        id_with_copy(transaction.id)
                        ui.button(
                            icon="edit",
                            on_click=lambda _, transaction_id=transaction.id: ui.navigate.to(
                                f"/transactions/{transaction_id}"
                            ),
                        )
                        DeleteButtonWithConfirmation(
                            icon="delete",
                            dialog_text=f"Вы действительно хотите удалить транзакцию {transaction.description} ({transaction.id})?",
                            on_delete_callback=partial(
                                confirm_deletion,
                                user_id=user.id,
                                transaction_id=transaction.id,
                            ),
                        )
                    with ui.row():
                        amount_with_gradient(transaction.amount)
                        if category.emoji_icon:
                            ui.label(category.emoji_icon).classes("text-2xl")
                        ui.label(category.name).classes("text-xl font-bold")
                    ui.label(transaction.description).classes("text-sm")
                    with ui.row():
                        with ui.column():
                            ui.label("Дата транзакции")
                            ui.label(transaction.timestamp).classes("text-sm")
                        with ui.column():
                            ui.label("Дата создания")
                            ui.label(transaction.created_at).classes("text-sm")
                        with ui.column():
                            ui.label("Дата обновления")
                            ui.label(transaction.updated_at).classes("text-sm")

        with ui.row():
            ui.pagination(
                min=1,
                max=pages,
                value=page,
                direction_links=True,
                on_change=lambda e: ui.navigate.to(
                    f"/transactions?page={e.value}&limit={limit}&search_text={search_text}"
                ),
            )
            ui.select(
                [5, 10, 20, 50],
                value=limit,
                on_change=lambda e: ui.navigate.to(f"/transactions?page=1&limit={e.value}&search_text={search_text}"),
            )

    with ui.page_sticky(x_offset=18, y_offset=18):
        ui.button("+", on_click=lambda: ui.navigate.to("/transactions/new")).props("fab")


@router.page("/transactions/new")
async def create_transaction(request: Request):
    user: DetailedUserSchema = request.state.user

    async def load_categories() -> list[CategorySchema]:
        _, categories = await CategoryManager().list_(user_id=user.id, limit=None, offset=0)
        return categories

    categories = await load_categories()

    async def validate_and_create(amount: float, description: str, category_id: str, date: str, time: str) -> None:
        if not category_id:
            return ui.notify("Выберите категорию", type="negative")
        timestamp = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M").astimezone(UTC)

        await TransactionManager().create(
            user_id=user.id, amount=amount, description=description, category_id=category_id, timestamp=timestamp
        )
        ui.navigate.to("/transactions")

    with ui.row():
        ui.button(icon="arrow_back", on_click=ui.navigate.back)
        ui.label("Создание новой транзакции")

    category = ui.select(
        {cat.id: f"{cat.emoji_icon or ''} {cat.name}" for cat in categories},
        label="Категория*",
    )
    amount = ui.number("Сумма*", value=0.0, precision=2, format="%.2f")
    description = ui.textarea("Описание")
    with ui.row():
        ui.label("Дата")
        date_picker = DatePickerButton()
        ui.label("Время")
        time_picker = TimePickerButton()

    ui.button(
        "Создать",
        on_click=lambda _: validate_and_create(
            amount=amount.value,
            description=description.value,
            category_id=category.value,
            date=date_picker.text,
            time=time_picker.text,
        ),
    )


@router.page("/transactions/{transaction_id}")
async def update_transaction(request: Request, transaction_id: str):
    user: DetailedUserSchema = request.state.user
    logger.info(f"Show /transactions/{transaction_id} page for user {user.id}")

    async def load_categories() -> list[CategorySchema]:
        _, categories = await CategoryManager().list_(user_id=user.id, limit=None, offset=0)
        return categories

    categories = await load_categories()
    transaction = await TransactionManager().get(user_id=user.id, transaction_id=transaction_id)

    async def validate_and_save(amount: float, description: str, category_id: str, date: str, time: str) -> None:
        if not category_id:
            return ui.notify("Выберите категорию", type="negative")
        timestamp = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M").astimezone(UTC)

        await TransactionManager().update(
            user_id=user.id,
            transaction_id=transaction.id,
            amount=amount,
            description=description,
            category_id=category_id,
            timestamp=timestamp,
        )
        ui.navigate.to("/transactions")

    with ui.row():
        ui.button(icon="arrow_back", on_click=ui.navigate.back)
        ui.label("Редактирование транзакции")

    category = ui.select(
        {cat.id: f"{cat.emoji_icon or ''} {cat.name}" for cat in categories},
        value=transaction.category_id,
        label="Категория*",
    )
    amount = ui.number("Сумма*", value=transaction.amount, precision=2, format="%.2f")
    description = ui.textarea("Описание", value=transaction.description)
    with ui.row():
        ui.label("Дата")
        date_picker = DatePickerButton()
        ui.label("Время")
        time_picker = TimePickerButton()

    with ui.row():
        ui.button(
            "Сохранить",
            on_click=lambda _: validate_and_save(
                amount=amount.value,
                description=description.value,
                category_id=category.value,
                date=date_picker.text,
                time=time_picker.text,
            ),
        )
