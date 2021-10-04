import sys
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from sectograph import resources, entities, datetime as dt  # FONT_ADJUST


FONT_ADJUST = 0 if sys.platform == "darwin" else -4


class DayEvent(QtWidgets.QWidget):
    def __init__(
        self,
        parent: QtWidgets.QWidget,
        theme: resources.Theme,
        theme_name: str,
        evt: entities.DayEvent,
        slot: int = 0,
    ) -> None:
        super().__init__(parent)
        self.theme = theme
        self.theme_name = theme_name
        self.evt = evt
        self.start = evt.start
        self.text = evt.text
        self.color = evt.color
        self.slot = slot

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        self.draw(QtGui.QPainter(self))

    def draw(self, qp: QtGui.QPainter) -> None:
        now = dt.app_now()
        theme = self.theme.get(self.theme_name, "events")

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        cr = min(cx, cy)

        qp.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing)
        qp.translate(cx, cy)
        qp.rotate(-90.0)

        # draw arc
        arc_sangle = -round((30.0 * self.slot) * 16)
        arc_mangle = -round((30.0 * now.hour / 24) * 16)
        arc_eangle = -round(30.0 * 16)

        color = QtGui.QColor(self.color)

        # past part of the event
        arc_color = color.darker()
        arc_color.setAlpha(100)
        past_arc_pen = QtGui.QPen(arc_color, 20)
        past_arc_pen.setCapStyle(QtCore.Qt.FlatCap)
        qp.setPen(past_arc_pen)
        qp.drawArc(-cr + 10, -cr + 10, 2 * cr - 20, 2 * cr - 20, arc_sangle, arc_mangle)

        # future part of the event
        arc_color = color.darker()
        future_arc_pen = QtGui.QPen(arc_color, 20)
        future_arc_pen.setCapStyle(QtCore.Qt.FlatCap)
        qp.setPen(future_arc_pen)
        qp.drawArc(
            -cr + 10,
            -cr + 10,
            2 * cr - 20,
            2 * cr - 20,
            arc_sangle + arc_mangle,
            arc_eangle - arc_mangle,
        )

        # print event text
        qp.rotate(30.0 * self.slot)
        qp.translate(cr, 0)
        qp.rotate(90.0)

        font = QtGui.QFont("Raleway", 12 + FONT_ADJUST)
        qp.setFont(font)
        metrics = qp.fontMetrics()
        qp.setPen(QtGui.QPen(QtGui.QColor(theme("font")), 1))

        # Qt doesn't support printing text following the curved path
        # so emulate this by printing one char by one

        total_angle = 0
        for ch in " " + self.text:
            sina_2 = metrics.boundingRect(ch + " ").width() / (2 * cr)
            angle = math.degrees(math.asin(sina_2) * 2)
            total_angle += angle

            if total_angle >= 25:
                ch = "…"
            qp.drawText(0, 0, 100, 20, QtCore.Qt.AlignVCenter, ch)
            if total_angle >= 25:
                break

            qp.translate(0, cr)
            qp.rotate(angle)
            qp.translate(0, -cr)
