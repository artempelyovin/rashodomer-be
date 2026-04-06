import logging

from nicegui import ui

from app_ui.dependencies import build_budget_controller
from app_ui.pages.budgets import render_budgets_page

logging.basicConfig(level=logging.INFO)

budget_controller = build_budget_controller()


@ui.page("/")
async def budgets_page() -> None:
    await render_budgets_page(budget_controller)


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Rashodomer")