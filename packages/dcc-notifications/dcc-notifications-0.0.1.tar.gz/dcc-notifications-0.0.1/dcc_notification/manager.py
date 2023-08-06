"""
The NotificationManager class
"""
from __future__ import annotations

import os

from typing import Callable

from PySide2 import QtWidgets, QtCore

from .notification_message import NotificationMessage
from .notification_wrapper import NotificationWrapper


def get_main_window() -> QtWidgets.QMainWindow:
    """ Get the main window of the application """
    for widget in QtWidgets.QApplication.instance().topLevelWidgets():
        if isinstance(widget, QtWidgets.QMainWindow):
            return widget
    raise RuntimeError("No main window found")


def get_main_window_geometry() -> QtCore.QRect:
    """ Get the geometry of the main window """
    return get_main_window().geometry()


class NotificationManager:
    """
    This is a singleton class that manages the notifications
    """
    _instance = None
    _initialized = False

    notifications: list[NotificationWrapper] = []

    @classmethod
    def reload(cls):
        cls._instance = super().__new__(cls)
        cls._instance.__init__()
        return cls._instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.set_style(None)

    def show_widget(self, widget: QtWidgets.QWidget, title: str = "", duration: float = 0):
        """ Show a widget as a notification """
        notification = NotificationWrapper(widget, title, self.style_str)
        notification.show(self._on_notification_closed, duration)

        self.notifications.append(notification)

        self._recalculate_positions()

    def show_information(self, title: str, message: str, buttons: list[tuple[str, Callable]] | None = None, duration: float = 5):
        """ Show an information notification """
        notification = NotificationMessage(message, buttons)
        self.show_widget(notification, title, duration)

    def _on_notification_closed(self, notification: NotificationWrapper):
        if notification in self.notifications:
            self.notifications.remove(notification)

        self._recalculate_positions()

    def _recalculate_positions(self):
        """ Recalculate the positions of all notifications """
        main_window_geo = get_main_window_geometry()
        height_offset = 0
        for notification in self.notifications:
            notification_size = notification.size()
            notification_position = QtCore.QPoint(
                main_window_geo.right() - notification_size.width() - 10,
                main_window_geo.bottom() - notification_size.height() - 10 - height_offset,
            )
            notification.setGeometry(QtCore.QRect(
                notification_position, notification_size))
            height_offset += notification_size.height() + 10

    def set_style(self, style: str | None):
        """ 
        Set the style for the notifications. The style set will be applied to all new notifications that are spawned.

        ### Parameters:
        - style: The style to use. This can be a string containing the style, or a path to a qss file containing the style.
        """
        if not style:
            self.style_str = ""
        elif os.path.isfile(style):
            with open(style, 'r', encoding="utf-8") as file:
                self.style_str = file.read()
        else:
            self.style_str = style

        # load the default style
        default_style_filename = os.path.join(os.path.dirname(__file__), "styles", "default.qss")
        with open(default_style_filename, 'r', encoding="utf-8") as file:
            self.style_str += file.read()
