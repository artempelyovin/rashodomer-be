import asyncio
from typing import Callable, Coroutine

from nicegui import ui
from nicegui.elements.button import Button
from nicegui.elements.dialog import Dialog


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

