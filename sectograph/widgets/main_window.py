from PyQt5 import QtCore, QtGui, QtWidgets
from sectograph import resources, widgets


# according to Qt documentation QMainWindow *must* contain central widget
# https://doc.qt.io/qt-5/qmainwindow.html#details
# so use just usual QWidget as a base class
class MainWindow(QtWidgets.QWidget):
    def __init__(self, app: widgets.Application, theme_name: str) -> None:
        super().__init__()
        self.app = app
        self.theme = app.theme
        self.theme_name = theme_name

        # place widgets
        self.face = widgets.Face(self, app.theme, theme_name)
        self.events_layer = widgets.EventsLayer(self, app.theme, theme_name)
        self.clock = widgets.Clock(self, app.theme, theme_name)
        self.hands = widgets.Hands(self, app.theme, theme_name)
        self.mouse_handler = widgets.MouseHandler(self, app)
        self.add_button = widgets.AddButton(self, app, app.theme, theme_name)
        self.about_button = widgets.AboutButton(self, app, app.theme, theme_name)

        # get events and set refresh events timer
        self.update_events()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_events)
        timer.setInterval(10 * 60 * 1000)  # once in 10 minutes
        timer.start()

        # setup main window view and behaviour
        self.initUI()

    def initUI(self) -> None:
        self.resize(400, 400)
        self.setMinimumSize(400, 400)
        self.setMaximumSize(400, 400)
        self.setWindowTitle("Sectograph")
        self.setWindowIcon(QtGui.QIcon(resources.Icons.color))

    def update_events(self):
        events = self.app.events_repository.get()
        day_events = self.app.day_events_repository.get()
        self.events_layer.update_events(events, day_events)
        self.mouse_handler.update_events(events, day_events)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        full = self.rect()
        small = QtCore.QRect(20, 20, self.width() - 40, self.height() - 40)

        # resize all children widgets
        self.face.setGeometry(small)
        self.events_layer.setGeometry(full)
        self.clock.setGeometry(small)
        self.hands.setGeometry(full)
        self.mouse_handler.setGeometry(full)

        # position for "add" and "help" buttons
        w, h = self.width(), self.height()
        x, y = w // 2, h // 2
        r = min(x, y)
        self.add_button.setGeometry(x + r - 50, y + r - 50, 40, 40)
        self.about_button.setGeometry(x - r - 40 + 50, y + r - 50, 40, 40)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        if key == QtCore.Qt.Key_Plus:
            self.app.edit_window.open_with_new()
        elif key == QtCore.Qt.Key_Question:
            self.app.about_window.show()
