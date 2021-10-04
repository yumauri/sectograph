from PyQt5 import QtCore, QtGui, QtWidgets
from sectograph import resources, datetime as dt, FONT_ADJUST


class Clock(QtWidgets.QWidget):
    def __init__(
        self, parent: QtWidgets.QWidget, theme: resources.Theme, theme_name: str
    ) -> None:
        super().__init__(parent)
        self.theme = theme
        self.theme_name = theme_name

        # refresh timer
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.repaint)
        timer.setInterval(500)  # half of a second
        timer.start()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        self.draw(QtGui.QPainter(self))

    def draw(self, qp: QtGui.QPainter) -> None:
        now = dt.app_now()
        theme = self.theme.get(self.theme_name, "center")

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        r = 40

        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.translate(cx, cy)

        # draw central disk
        qp.setPen(QtCore.Qt.NoPen)
        center_color = QtGui.QColor(theme("color"))
        # center_color.setAlpha(200)
        qp.setBrush(QtGui.QBrush(center_color))
        qp.drawEllipse(-r, -r, 2 * r, 2 * r)

        # print current date time
        qp.setPen(QtGui.QPen(QtGui.QColor(theme("font")), 2))
        qp.setFont(QtGui.QFont("Raleway", 22 + FONT_ADJUST, QtGui.QFont.Black))
        qp.drawText(
            -r,
            -r,
            2 * r,
            int(1.5 * r),
            QtCore.Qt.AlignCenter,
            f"{now.hour}:{now.strftime('%M')}",
        )

        qp.setFont(QtGui.QFont("Raleway", 18 + FONT_ADJUST))
        qp.drawText(
            -r,
            int(-r * 0.5),
            2 * r,
            int(1.5 * r),
            QtCore.Qt.AlignCenter,
            f"{now.strftime('%a')} {now.day}".lower(),
        )
