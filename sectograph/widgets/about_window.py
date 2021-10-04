from PyQt5 import QtCore, QtGui, QtWidgets  # , uic
from sectograph import widgets
from .about_window_ui import Ui_AboutForm


# class AboutWindow(QtWidgets.QWidget):
class AboutWindow(QtWidgets.QWidget, Ui_AboutForm):
    app: widgets.Application

    def __init__(self, app: widgets.Application, theme_name: str) -> None:
        super().__init__(app.main_window)
        self.app = app
        # uic.loadUi('sectograph/widgets/about_window_ui.ui', self)
        self.setupUi(self)
        self.initUI()

    def initUI(self) -> None:
        self.setWindowFlags(QtCore.Qt.Tool)
        self.close_PushButton.clicked.connect(self.close)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()

    def showEvent(self, event):
        rect = self.parent().geometry()
        x = rect.x() + rect.width() // 2 - self.width() // 2
        y = rect.y()
        self.move(x, y)
        super().showEvent(event)
        self.activateWindow()
