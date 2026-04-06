from nicegui import ui

import fe.pages.budgets  # noqa: F401


def run_app() -> None:
    ui.run(title="Расходомер", port=8080, reload=True)


if __name__ in {"__main__", "__mp_main__"}:
    run_app()
