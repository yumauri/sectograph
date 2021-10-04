from PyQt5 import QtCore, QtGui, QtWidgets
from sectograph import resources, datetime as dt


class Hands(QtWidgets.QWidget):
    def __init__(
        self, parent: QtWidgets.QWidget, theme: resources.Theme, theme_name: str
    ) -> None:
        super().__init__(parent)
        self.theme = theme
        self.theme_name = theme_name

        # refresh timer
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.repaint)
        theme = self.theme.get(self.theme_name, "hands")
        if theme("smooth"):
            timer.setInterval(50)  # 1/20 of a second
        else:
            timer.setInterval(250)  # quarter of a second
        timer.start()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        self.draw(QtGui.QPainter(self))

    def draw(self, qp: QtGui.QPainter) -> None:
        now = dt.app_now()
        theme = self.theme.get(self.theme_name, "hands")

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        sr = 45
        er = min(cx, cy)

        qp.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing)
        qp.translate(cx, cy)
        qp.rotate(-90.0)

        # first half of hour hand
        qp.save()
        qp.rotate(30.0 * (now.hour + now.minute / 60.0))
        hscolor = QtGui.QColor(theme("hour", 0))
        hpen = QtGui.QPen(hscolor, theme("hour", 1))
        hpen.setCapStyle(QtCore.Qt.FlatCap)
        qp.setPen(hpen)
        qp.drawLine(sr, 0, round(er * 0.6), 0)

        # second half of hour hand
        hecolor = QtGui.QColor(theme("hour", 0))
        hecolor.setAlpha(100)
        hpen = QtGui.QPen(hecolor, theme("hour", 1))
        hpen.setStyle(QtCore.Qt.CustomDashLine)
        hpen.setDashPattern([1, 1])
        hpen.setDashOffset(2)
        hpen.setCapStyle(QtCore.Qt.FlatCap)
        qp.setPen(hpen)
        qp.drawLine(round(er * 0.6), 0, er - 20, 0)

        # hour hand cap
        qp.setPen(QtCore.Qt.NoPen)
        # back_color = QtGui.QColor(theme("back"))
        # back_color.setAlpha(20)
        qp.setBrush(QtGui.QBrush(hscolor))

        qp.drawEllipse(er - 26, -8, 16, 16)

        qp.restore()

        # two hours back line
        qp.save()
        qp.rotate(30.0 * ((now.hour - 2) + now.minute / 60.0))
        bcolor = QtGui.QColor(theme("back", 0))
        bpen = QtGui.QPen(bcolor, theme("back", 1))
        bpen.setStyle(QtCore.Qt.DashLine)
        qp.setPen(bpen)
        qp.drawLine(sr, 0, er, 0)
        qp.restore()

        # minute hand
        qp.save()
        qp.rotate(6.0 * (now.minute + now.second / 60.0))
        mcolor = QtGui.QColor(theme("minute", 0))
        mpen = QtGui.QPen(mcolor, theme("minute", 1))
        mpen.setStyle(QtCore.Qt.DotLine)
        qp.setPen(mpen)
        qp.drawLine(sr, 0, er, 0)
        qp.restore()

        # second hand
        qp.save()
        if theme("smooth"):
            qp.rotate(6.0 * (now.second + now.microsecond / 1e6))
        else:
            qp.rotate(6.0 * now.second)
        scolor = QtGui.QColor(theme("second", 0))
        scolor.setAlpha(100)
        spen = QtGui.QPen(scolor, theme("second", 1))
        spen.setStyle(QtCore.Qt.DashLine)
        qp.setPen(spen)
        qp.drawLine(sr, 0, er, 0)
        qp.restore()
