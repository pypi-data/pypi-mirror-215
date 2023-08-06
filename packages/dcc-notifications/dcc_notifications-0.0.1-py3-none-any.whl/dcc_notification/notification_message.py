""" 
Simple Message
"""

from __future__ import annotations

from typing import Callable

from PySide2 import QtWidgets


class NotificationMessage(QtWidgets.QWidget):
    def __init__(self, message: str, buttons: list[tuple[str, Callable]] | None = None):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 5)

        message_label = QtWidgets.QLabel(message)
        # Wrap the text
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        if buttons:
            button_layout = QtWidgets.QHBoxLayout()

            spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            button_layout.addItem(spacer)

            for button_text, callback in buttons:
                button = QtWidgets.QPushButton(button_text)
                button.clicked.connect(callback)
                button_layout.addWidget(button)

            layout.addLayout(button_layout)

    def on_button_click(self, callback: Callable) -> None:
        if callback():
            self.close()
