import logging
from functools import partial
from math import ceil

from nicegui import APIRouter, ui
from nicegui.elements.input import Input
from nicegui.elements.number import Number
from nicegui.elements.textarea import Textarea
from starlette.requests import Request

from managers.budget import BudgetManager
from models.user import DetailedUserSchema
from ui.components.buttons import DeleteButtonWithConfirmation
from ui.components.labels import amount_with_gradient, id_with_copy

logger = logging.getLogger(__name__)
router = APIRouter()


@router.page("/budgets")
async def list_budgets(request: Request, page: int = 1, limit: int = 10):
    async def confirm_deletion(user_id: str, budget_id: str) -> None:
        await BudgetManager().delete(user_id=user_id, budget_id=budget_id)
        logger.info(f"Successful delete budget {budget_id} for user {user_id}")
        ui.navigate.to("/budgets")

    user: DetailedUserSchema = request.state.user
    logger.info(f"Show /budgets page for user {user.id} with {page=}, {limit=}")

    offset = (page - 1) * limit
    total, budgets = await BudgetManager().list_(user_id=user.id, limit=limit, offset=offset)
    logger.debug(f"Get {len(budgets)} budgets, {total=}")

    pages = ceil(total / limit) or 1

    if len(budgets) == 0:
        ui.label("У вас ещё нет бюджетов...")
        ui.label("Самое время создать первый бюджет!")
    else:
        with ui.column():
            for budget in budgets:
                with ui.card():
                    with ui.row():
                        id_with_copy(budget.id)
                        ui.button(
                            icon="edit", on_click=lambda _, budget_id=budget.id: ui.navigate.to(f"/budgets/{budget_id}")
                        )
                        DeleteButtonWithConfirmation(
                            icon="delete",
                            dialog_text=f"Вы действительно хотите удалить бюджет {budget.name} ({budget.id})?",
                            on_delete_callback=partial(confirm_deletion, user_id=user.id, budget_id=budget.id),
                        )
                    with ui.row():
                        ui.label(budget.name).classes("text-xl font-bold")
                        amount_with_gradient(budget.amount)
                    ui.label(budget.description).classes("text-sm")
                    with ui.row():
                        with ui.column():
                            ui.label("Дата создания")
                            ui.label(budget.created_at).classes("text-sm")
                        with ui.column():
                            ui.label("Дата обновления")
                            ui.label(budget.updated_at).classes("text-sm")
        with ui.row():
            ui.pagination(
                min=1,
                max=pages,
                value=page,
                direction_links=True,
                on_change=lambda event: ui.navigate.to(f"/budgets?page={event.value}&limit={limit}"),
            )
            ui.select(
                [5, 10, 20, 50],
                value=limit,
                on_change=lambda event: ui.navigate.to(f"/budgets?page=1&limit={event.value}"),
            )
    with ui.page_sticky(x_offset=18, y_offset=18):
        ui.button("+", on_click=lambda: ui.navigate.to("/budgets/new")).props("fab")


@router.page("/budgets/new")
async def create_budget(request: Request):
    user: DetailedUserSchema = request.state.user

    async def validate_and_create(name: str, description: str, amount: float) -> None:
        if not name:
            return ui.notify("Заполните название", type="negative")
        await BudgetManager().create(user_id=user.id, name=name, description=description, amount=amount)
        ui.navigate.to("/budgets")

    with ui.row():
        ui.button(icon="arrow_back", on_click=ui.navigate.back)
        ui.label("Создание нового бюджета")
    name = ui.input("Название*")
    description = ui.textarea("Описание")
    amount = ui.number("Сумма", value=0.0, precision=5)
    ui.button(
        "Создать",
        on_click=lambda _: validate_and_create(name=name.value, description=description.value, amount=amount.value),
    )


@router.page("/budgets/{budget_id}")
async def update_budget(request: Request, budget_id: str):
    user: DetailedUserSchema = request.state.user
    logger.info(f"Show /budgets/{budget_id} page for user {user.id}")

    budget = await BudgetManager().get(user_id=user.id, budget_id=budget_id)

    async def validate_and_save(name: Input, description: Textarea, amount: Number) -> None:
        if not name.value:
            return ui.notify("Заполните название", type="negative")
        await BudgetManager().update(
            user_id=user.id, budget_id=budget.id, name=name.value, description=description.value, amount=amount.value
        )
        ui.navigate.to("/budgets")

    with ui.row():
        ui.button(icon="arrow_back", on_click=ui.navigate.back)
        ui.label("Редактирование бюджета")

    name = ui.input("Название", value=budget.name)
    description = ui.textarea("Описание", value=budget.description)
    amount = ui.number("Сумма", value=budget.amount, precision=5)
    ui.button("Сохранить", on_click=lambda _: validate_and_save(name=name, description=description, amount=amount))
