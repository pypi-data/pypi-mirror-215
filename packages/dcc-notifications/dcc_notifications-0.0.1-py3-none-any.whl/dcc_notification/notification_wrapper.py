""" 
Notification
"""

from __future__ import annotations

from typing import Callable

from PySide2 import QtWidgets, QtCore


class NotificationWrapper(QtWidgets.QWidget):
    def __init__(self, content_widget: QtWidgets.QWidget, title: str = "", style: str = ""):  # pylint: disable=useless-super-delegation
        super().__init__()

        self.setStyleSheet(style)
        self.setFixedSize(300, 100)

        self.timer = None
        self.on_close = None

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        wrapper_layout = QtWidgets.QVBoxLayout()
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)

        # Take the layout, and create a new main layout with a custom close button, and the original layout
        top_bar_widget = QtWidgets.QWidget()
        top_bar_widget.setObjectName("topBar")
        top_bar_layout = QtWidgets.QHBoxLayout()
        top_bar_layout.setContentsMargins(10, 0, 10, 0)
        top_bar_widget.setFixedHeight(25)
        top_bar_widget.setLayout(top_bar_layout)

        title_label = QtWidgets.QLabel(title)
        title_label.setObjectName("title")
        top_bar_layout.addWidget(title_label)

        close_button = QtWidgets.QPushButton("X", self)
        close_button.setObjectName("closeButton")
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(self.close)
        top_bar_layout.addWidget(close_button)

        wrapper_layout.addWidget(top_bar_widget)
        wrapper_layout.addWidget(content_widget)

        self.setLayout(wrapper_layout)

    def show(self, on_close: Callable[[NotificationWrapper], None], duration: float = 0) -> None:

        self.on_close = on_close

        # Close the notification after the set duration
        if duration > 0:
            self.timer = QtCore.QTimer()
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.close)
            self.timer.start(int(duration * 1000))

        return super().show()

    def close(self) -> bool:
        if self.on_close is not None:
            self.on_close(self)

        if self.timer is not None:
            self.timer.stop()

        return super().close()
