from __future__ import annotations  # to avoid circular dependencies, need python 3.7+
from PyQt5 import QtWidgets
from sectograph import resources, database, repositories, widgets


class Application(QtWidgets.QApplication):
    theme: resources.Theme
    theme_name: str
    font: resources.Font
    sound: resources.Sound

    db: database.Database
    events_repository: repositories.Event
    day_events_repository: repositories.DayEvent

    main_window: widgets.MainWindow
    edit_window: widgets.EditWindow
    about_window: widgets.AboutWindow
    tray_widget: widgets.SysTray

    def __init__(self, args: list[str], theme_name: str = "default"):
        super().__init__(args)
        # self.setQuitOnLastWindowClosed(False)

        # from Qt documentation:
        # > This is a private signal. It can be used in signal connections but cannot be emitted by the user.
        self.aboutToQuit.connect(self.about_to_quit)

        # load theme
        self.theme = resources.Theme()
        self.theme_name = theme_name

        # load extra font
        self.font = resources.Font("raleway")

        # load sounds effects
        self.sound = resources.Sound()

        # connect to database
        self.db = database.Database()
        self.events_repository = repositories.Event(self.db)
        self.day_events_repository = repositories.DayEvent(self.db)
        self.colors_repository = repositories.Color(self.db)

    def about_to_quit(self):
        self.db.close()
