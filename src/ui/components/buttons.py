import asyncio
from datetime import UTC, datetime
from typing import Callable, Coroutine

from nicegui import ui
from nicegui.elements.button import Button
from nicegui.elements.date import Date
from nicegui.elements.dialog import Dialog
from nicegui.elements.time import Time


class DeleteButtonWithConfirmation(Button):
    def __init__(self, *args, dialog_text: str, on_delete_callback: Callable | Coroutine, **kwargs) -> None:
        self._dialog_text = dialog_text
        self._dialog = Dialog()
        self._on_delete_callback = on_delete_callback
        super().__init__(*args, on_click=self._dialog.open, **kwargs)

        self.setup_ui()

    def setup_ui(self) -> None:
        with self._dialog, ui.card():
            ui.label(self._dialog_text)

            with ui.row():
                ui.button("Да", on_click=self.handle_confirmation)
                ui.button("Нет", on_click=self._dialog.close)

    async def handle_confirmation(self):
        self._dialog.close()
        result = self._on_delete_callback()
        if asyncio.iscoroutine(result):
            await result


class DatePickerButton(Button):
    def __init__(self, *args, **kwargs) -> None:
        default_date = datetime.now(tz=UTC).date().strftime("%Y-%m-%d")
        self._dialog = Dialog()

        super().__init__(*args, text=default_date, on_click=self._dialog.open, **kwargs)
        with self._dialog, ui.card():
            self._date = Date(value=default_date)
            with ui.row():
                ui.button("Ок", on_click=self.handle_confirmation)
                ui.button("Отмена", on_click=self._dialog.close)

    def handle_confirmation(self):
        self._dialog.close()
        self.text = self._date.value


class TimePickerButton(Button):
    def __init__(self, *args, **kwargs) -> None:
        default_time = datetime.now(tz=UTC).strftime("%H:%M")
        self._dialog = Dialog()

        super().__init__(*args, text=default_time, on_click=self._dialog.open, **kwargs)
        with self._dialog, ui.card():
            self._time = Time(value=default_time).props("format24h now-btn")
            with ui.row():
                ui.button("Ок", on_click=self.handle_confirmation)
                ui.button("Отмена", on_click=self._dialog.close)

    def handle_confirmation(self):
        self._dialog.close()
        self.text = self._time.value
