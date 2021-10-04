from PyQt5 import QtCore, QtGui, QtWidgets
from sectograph import resources, datetime as dt, FONT_ADJUST


class Face(QtWidgets.QWidget):
    def __init__(
        self, parent: QtWidgets.QWidget, theme: resources.Theme, theme_name: str
    ) -> None:
        super().__init__(parent)
        self.theme = theme
        self.theme_name = theme_name

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        self.draw(QtGui.QPainter(self))

    def draw(self, qp: QtGui.QPainter) -> None:
        theme = self.theme.get(self.theme_name, "face")

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        r = min(cx, cy)
        cr = round(r * 0.96) - 5
        mr = 45

        qp.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing)
        qp.translate(cx, cy)

        # draw big background disk
        qp.setPen(QtCore.Qt.NoPen)
        back_color = QtGui.QColor(theme("back"))
        back_color.setAlpha(20)
        qp.setBrush(QtGui.QBrush(back_color))
        qp.drawEllipse(-cr, -cr, 2 * cr, 2 * cr)

        # # cut out center disk
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOut)
        qp.drawEllipse(-mr, -mr, 2 * mr, 2 * mr)
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)

        # draw ticks
        qp.save()
        hour_pen = QtGui.QPen(
            QtGui.QColor(theme("tick", "hour", 0)), theme("tick", "hour", 1)
        )
        hour_pen.setCapStyle(QtCore.Qt.FlatCap)
        minute_pen = QtGui.QPen(
            QtGui.QColor(theme("tick", "minute", 0)), theme("tick", "minute", 1)
        )
        minute_pen.setCapStyle(QtCore.Qt.FlatCap)
        for m in range(60):
            if m % 5 == 0:
                qp.setPen(hour_pen)
                qp.drawLine(round(r * 0.96), 0, r, 0)
            else:
                qp.setPen(minute_pen)
                qp.drawLine(round(r * 0.98), 0, r, 0)
            qp.rotate(6.0)
        qp.restore()

        # draw hours
        qp.save()
        qp.setPen(QtGui.QPen(QtGui.QColor(theme("hours")), 2))
        qp.setBrush(QtGui.QBrush(QtGui.QColor(theme("hours"))))
        qp.setFont(QtGui.QFont("Raleway", 20 + FONT_ADJUST, QtGui.QFont.Bold))
        qp.rotate(-90.0)
        for h in range(12):
            qp.translate(r * 0.96 - 20, 0)
            qp.rotate(90.0 - h * 30.0)
            if h == 0:
                if 2 <= dt.app_now().hour < 14:
                    # draw sun instead of 12 hour
                    qp.drawEllipse(-4, -4, 8, 8)
                    for _ in range(9):
                        qp.drawLine(8, 0, 10, 0)
                        qp.rotate(45.0)
                    qp.rotate(-45.0)
                else:
                    # draw moon instead of 12 hour
                    qp.setPen(QtGui.QPen(QtGui.QColor(theme("hours")), 1))
                    qp.drawArc(-12, -9, 14, 18, -90 * 16, 180 * 16)
                    qp.drawArc(-12, -9, 15, 18, -90 * 16, 180 * 16)
                    qp.drawArc(-12, -9, 16, 18, -90 * 16, 180 * 16)
                    qp.drawArc(-12, -9, 17, 18, -90 * 16, 180 * 16)
                    qp.drawArc(-12, -9, 18, 18, -90 * 16, 180 * 16)
                    qp.setPen(QtGui.QPen(QtGui.QColor(theme("hours")), 2))
            else:
                # draw hour number
                qp.drawText(-10, -15, 20, 25, QtCore.Qt.AlignCenter, str(h))
            qp.rotate(-90.0 + h * 30.0)
            qp.translate(-r * 0.96 + 20, 0)
            qp.rotate(30.0)
        qp.restore()

        # draw grey hour lines
        qp.save()
        hourlines_color = QtGui.QColor(theme("line", "hour", 0))
        hourlines_color.setAlpha(100)
        pen = QtGui.QPen(hourlines_color, theme("line", "hour", 1))
        for m in range(12):
            qp.setPen(pen)
            qp.drawLine(50, 0, round(r * 0.96) - 45, 0)
            qp.rotate(30.0)
        qp.restore()
