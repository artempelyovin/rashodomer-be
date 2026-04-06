import logging
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from nicegui import ui

from app_ui.controllers.budget import BudgetCrudController
from domain.errors import BudgetNotFoundError, DomainError, EmptyNameError, NegativeBalanceError
from domain.models.budget import Budget

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class BudgetPageState:
    editing_budget_id: str | None = None


def _parse_balance(raw_value: str | None) -> Decimal:
    normalized_value = (raw_value or "").strip().replace(",", ".")
    if not normalized_value:
        raise InvalidOperation
    return Decimal(normalized_value)


async def render_budgets_page(controller: BudgetCrudController) -> None:
    state = BudgetPageState()

    async def refresh_budgets() -> None:
        budgets_container.clear()
        budgets = await controller.list_budgets()

        with budgets_container:
            if not budgets:
                ui.label("Бюджетов пока нет.")
                return

            for budget in budgets:
                render_budget_card(budget)

    def open_create_dialog() -> None:
        state.editing_budget_id = None
        name_input.value = ""
        balance_input.value = "0"
        description_input.value = ""
        form_dialog.open()

    def open_edit_dialog(budget: Budget) -> None:
        state.editing_budget_id = budget.id
        name_input.value = budget.name
        balance_input.value = str(budget.balance)
        description_input.value = budget.description or ""
        form_dialog.open()

    async def save_budget() -> None:
        name = (name_input.value or "").strip()
        description = description_input.value or None

        try:
            balance = _parse_balance(balance_input.value)
        except InvalidOperation:
            ui.notify("Введите корректный баланс.", type="negative")
            return

        try:
            if state.editing_budget_id is None:
                await controller.create_budget(name=name, balance=balance, description=description)
                ui.notify("Бюджет создан.", type="positive")
            else:
                await controller.update_budget(
                    budget_id=state.editing_budget_id,
                    name=name,
                    balance=balance,
                    description=description,
                )
                ui.notify("Бюджет обновлён.", type="positive")
        except EmptyNameError:
            ui.notify("Укажите название бюджета.", type="negative")
            return
        except NegativeBalanceError:
            ui.notify("Баланс не может быть отрицательным.", type="negative")
            return
        except BudgetNotFoundError:
            ui.notify("Бюджет не найден.", type="negative")
            return
        except DomainError:
            logger.exception("Failed to save budget")
            ui.notify("Не удалось сохранить бюджет.", type="negative")
            return

        form_dialog.close()
        await refresh_budgets()

    async def delete_budget(budget_id: str) -> None:
        try:
            await controller.delete_budget(budget_id)
        except BudgetNotFoundError:
            ui.notify("Бюджет не найден.", type="negative")
            return
        except DomainError:
            logger.exception("Failed to delete budget %s", budget_id)
            ui.notify("Не удалось удалить бюджет.", type="negative")
            return

        ui.notify("Бюджет удалён.", type="positive")
        await refresh_budgets()

    def render_budget_card(budget: Budget) -> None:
        with ui.card():
            ui.label(budget.name)
            ui.label(f"Баланс: {budget.balance}")
            ui.label(budget.description or "Без описания")

            with ui.row():
                ui.button("Изменить", on_click=lambda budget=budget: open_edit_dialog(budget))

                async def on_delete() -> None:
                    await delete_budget(budget.id)

                ui.button("Удалить", on_click=on_delete)

    with ui.column():
        ui.label("Бюджеты")

        with ui.row():
            ui.button("Добавить бюджет", on_click=open_create_dialog)
            ui.button("Обновить список", on_click=refresh_budgets)

        budgets_container = ui.column()

    with ui.dialog() as form_dialog, ui.card():
        ui.label("Бюджет")
        name_input = ui.input("Название")
        balance_input = ui.input("Баланс", value="0")
        description_input = ui.textarea("Описание")

        with ui.row():
            ui.button("Отмена", on_click=form_dialog.close)
            ui.button("Сохранить", on_click=save_budget)

    await refresh_budgets()