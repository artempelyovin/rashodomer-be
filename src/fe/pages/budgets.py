import logging
from decimal import Decimal

from nicegui import ui

from domain.errors import DomainError
from domain.models.budget import Budget
from fe.dependencies import (
    HARDCODED_USER_ID,
    create_budget_uc,
    delete_budget_uc,
    list_budgets_uc,
    update_budget_uc
)

logger = logging.getLogger(__name__)


class BudgetsPage:
    def __init__(self) -> None:
        self._budgets: list[Budget] = []
        # Состояние формы (None если создаем новый)
        self._editing_budget_id: str | None = None

    async def _load_data(self) -> None:
        self._budgets = await list_budgets_uc.execute(user_id=HARDCODED_USER_ID)
        self.render_budgets_table.refresh()

    async def _on_save(self, name: str, balance: float, description: str) -> None:
        try:
            desc_val = description if description else None
            balance_dec = Decimal(str(balance))

            if self._editing_budget_id:
                await update_budget_uc.execute(
                    budget_id=self._editing_budget_id,
                    name=name,
                    balance=balance_dec,
                    description=desc_val,
                )
                ui.notify("Бюджет обновлен")
            else:
                await create_budget_uc.execute(
                    name=name,
                    balance=balance_dec,
                    user_id=HARDCODED_USER_ID,
                    description=desc_val,
                )
                ui.notify("Бюджет создан")

            self._dialog.close()
            await self._load_data()
        except DomainError as e:
            logger.warning("Domain error while saving budget: %s", e)
            ui.notify(str(e), type="negative")
        except Exception:
            logger.exception("Unexpected error while saving budget")
            ui.notify("Произошла системная ошибка", type="negative")

    async def _on_delete(self, budget_id: str) -> None:
        try:
            await delete_budget_uc.execute(budget_id)
            ui.notify("Бюджет удален")
            await self._load_data()
        except DomainError as e:
            logger.warning("Domain error while deleting budget: %s", e)
            ui.notify(str(e), type="negative")
        except Exception:
            logger.exception("Unexpected error while deleting budget")
            ui.notify("Произошла системная ошибка", type="negative")

    def _open_form_dialog(self, budget: Budget | None = None) -> None:
        self._editing_budget_id = budget.id if budget else None

        self._dialog.clear()
        with self._dialog, ui.card():
            ui.label("Редактирование бюджета" if budget else "Новый бюджет")

            name_input = ui.input("Название", value=budget.name if budget else "")
            balance_input = ui.number("Баланс", value=float(budget.balance) if budget else 0.0, format="%.2f")
            desc_input = ui.input("Описание", value=budget.description if budget and budget.description else "")

            with ui.row():
                ui.button("Отмена", on_click=self._dialog.close)
                ui.button(
                    "Сохранить",
                    on_click=lambda: self._on_save(name_input.value, balance_input.value, desc_input.value),
                )
        self._dialog.open()

    @ui.refreshable
    def render_budgets_table(self) -> None:
        if not self._budgets:
            ui.label("У вас пока нет бюджетов.")
            return

        with ui.row():
            for budget in self._budgets:
                with ui.card():
                    ui.label(budget.name)
                    ui.label(f"Баланс: {budget.balance}")
                    if budget.description:
                        ui.label(budget.description)

                    with ui.row():
                        ui.button("Изменить", on_click=lambda b=budget: self._open_form_dialog(b))
                        ui.button("Удалить", on_click=lambda b=budget: self._on_delete(b.id), color="red")

    def build(self) -> None:
        ui.label("Мои бюджеты")
        ui.button("Добавить бюджет", on_click=lambda: self._open_form_dialog())

        self._dialog = ui.dialog()
        self.render_budgets_table()

        # Запускаем загрузку данных при открытии страницы
        ui.timer(0, self._load_data, once=True)


@ui.page("/")
def budgets_page_route() -> None:
    page = BudgetsPage()
    page.build()
