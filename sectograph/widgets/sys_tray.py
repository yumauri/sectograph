import sys
import platform
import functools
from PyQt5 import QtCore, QtGui, QtWidgets
from sectograph import widgets, resources, datetime as dt


class SysTray(QtWidgets.QSystemTrayIcon):
    def __init__(self, app: widgets.Application, theme_name: str) -> None:
        super().__init__()
        self.app = app
        self.theme = app.theme
        self.theme_name = theme_name

        # get events and set refresh events timer
        self.update_alerts()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_alerts)
        timer.setInterval(60 * 1000)  # once in a minute
        timer.start()

        # for windows and linux use color icon
        # for macos - monochrome one
        icon = QtGui.QIcon(resources.Icons.color)
        if sys.platform == "darwin":
            from distutils.version import LooseVersion

            if LooseVersion(platform.mac_ver()[0]) >= LooseVersion("10.14"):
                icon = QtGui.QIcon(resources.Icons.bw_fill)
                icon.setIsMask(True)
        self.setIcon(icon)
        self.setToolTip("Sectograph")

        # add context menu
        menu = QtWidgets.QMenu()
        new_event_action = QtWidgets.QAction("New event", menu)
        new_event_action.triggered.connect(self.add_event)
        menu.addAction(new_event_action)
        menu.addSeparator()
        about_action = QtWidgets.QAction("About", menu)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)
        quit_action = QtWidgets.QAction("Quit", menu)
        quit_action.triggered.connect(app.quit)
        menu.addAction(quit_action)
        self.setContextMenu(menu)
        self.activated.connect(self.on_activated)

    def update_alerts(self):
        now = dt.app_now()
        alerts = self.app.events_repository.get_minute_alerts()
        for alert in alerts:
            left = (alert["time"] - now).total_seconds()
            QtCore.QTimer.singleShot(
                left * 1000,
                functools.partial(self.alert, alert["text"], alert["sound"]),
            )

    def alert(self, text, sound):
        self.showMessage("Event notification", text)
        if sound:
            self.app.sound.play(sound)

    def show_main_window(self):
        # print(self.geometry())
        # pos = self.geometry().topRight()
        # x, y = pos.x() - self.app.main_window.width() // 2, pos.y() - self.app.main_window.height()
        # self.app.main_window.move(x, y)
        self.app.main_window.show()

    def on_activated(self, reason: QtWidgets.QSystemTrayIcon.ActivationReason):
        self.show_main_window()
        self.app.main_window.focusWidget()

    def add_event(self):
        self.show_main_window()
        self.app.edit_window.open_with_new()
        self.app.edit_window.focusWidget()

    def show_about(self):
        self.show_main_window()
        self.app.about_window.show()
        self.app.about_window.focusWidget()
