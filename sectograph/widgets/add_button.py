from PyQt5 import QtCore, QtGui, QtWidgets
from sectograph import resources, widgets, FONT_ADJUST


class AddButton(QtWidgets.QPushButton):
    app: widgets.Application
    theme: resources.Theme
    theme_name: str

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        app: widgets.Application,
        theme: resources.Theme,
        theme_name: str,
    ) -> None:
        super().__init__(parent)
        self.app = app
        self.theme = theme
        self.theme_name = theme_name

        font = QtGui.QFont("Arial", 24 + FONT_ADJUST)
        font.setWeight(QtGui.QFont.Medium)
        self.setFont(font)
        self.setText("+")
        self.setCursor(QtCore.Qt.PointingHandCursor)

        self.clicked.connect(self.add_event)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        theme = self.theme.get(self.theme_name, "buttons")

        rect = self.rect()
        side = rect.width()
        bigger_rect = QtCore.QRect(-2, -2, side + 4, side + 4)
        self.setStyleSheet(
            f"""
            border-radius:{side // 2}px;
            border:2px solid {theme("border")};
            background-color: {theme("background")};
        """
        )
        self.setMask(QtGui.QRegion(bigger_rect, QtGui.QRegion.Ellipse))

    def add_event(self):
        self.app.edit_window.open_with_new()
