from nicegui import ui


def id_with_copy(id_: str) -> None:
    """Компонент ID + кнопка копирования"""
    with ui.row().classes("items-center gap-1"):
        ui.label(id_).classes("font-mono text-sm")
        ui.button(icon="content_copy", color="gray").classes("opacity-50 hover:opacity-100 p-1").props("flat dense").on(
            "click",
            lambda: [
                ui.run_javascript(f"navigator.clipboard.writeText(`{id_}`)"),
                ui.notify(f"Скопировано: {id_}", type="positive"),
            ],
        )


def amount_with_gradient(amount: float, max_amount: float = 50000) -> None:
    """
    Компонент для отображения суммы с динамическим цветом

    :param amount: сумма для отображения
    :param max_amount: максимальная сумма (для градации цвета)
    """
    normalized = min(amount / max_amount, 1.0)
    # От hue=120 (зелёный) до hue=60 (жёлто-зелёный) при приближении к 0
    hue = 60 + (120 - 60) * normalized
    color = f"hsl({hue}, 100%, 40%)"
    ui.label(f"{amount:,.2f} ₽").classes("text-xl font-bold").style(f"color: {color}")
