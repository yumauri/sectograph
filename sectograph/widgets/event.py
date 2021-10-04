import sys
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from sectograph import resources, entities, datetime as dt  # FONT_ADJUST


FONT_ADJUST = 0 if sys.platform == "darwin" else -4


def time(hour, minute=None):
    if minute is None and type(hour) is dt.datetime:
        return time(hour.hour, hour.minute)
    return str(hour) + ":" + str(minute).rjust(2, "0")


def human_duration(seconds: float) -> str:
    minutes = math.ceil(seconds / 60)
    hours, minutes = int(minutes / 60), int(minutes % 60)
    if hours == 0:
        return str(minutes)
    if hours == 1 and minutes == 0:
        return "60"
    else:
        return time(hours, minutes)


class Event(QtWidgets.QWidget):
    def __init__(
        self,
        parent: QtWidgets.QWidget,
        theme: resources.Theme,
        theme_name: str,
        evt: entities.Event,
        slot: int = 0,
    ) -> None:
        super().__init__(parent)
        self.theme = theme
        self.theme_name = theme_name
        self.evt = evt

        # adjust date for repeated events
        today = dt.app_today()
        if evt.repeat:
            self.evt_start = evt.start.replace(
                year=today.year, month=today.month, day=today.day
            )
            self.evt_finish = evt.finish.replace(
                year=today.year, month=today.month, day=today.day
            )
            self.evt_finish += evt.finish.date() - evt.start.date()
        else:
            self.evt_start = evt.start
            self.evt_finish = evt.finish

        self.start = self.evt_start
        self.finish = self.evt_finish
        self.duration = self.evt_finish - self.evt_start
        self.text = evt.text
        self.color = evt.color
        self.slot = slot

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        self.draw(QtGui.QPainter(self))

    def draw(self, qp: QtGui.QPainter) -> None:
        now = dt.app_now()
        past2h = now - dt.timedelta(hours=2)
        past1h = now - dt.timedelta(hours=1)
        future10h = now + dt.timedelta(hours=10)
        theme = self.theme.get(self.theme_name, "events")

        # check if event we should draw event at all
        if self.finish <= past2h or self.start > future10h:
            return

        # adjust start and finish of event
        self.start = max(past2h, self.start)
        self.finish = min(future10h, self.finish)
        self.duration = self.finish - self.start

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        cr = min(cx, cy)
        mr = 45

        qp.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing)
        qp.translate(cx, cy)
        qp.rotate(-90.0)

        sangle = -round(30.0 * (self.start.hour + self.start.minute / 60.0) * 16)
        eangle = -round(30.0 * (self.duration.total_seconds() / 3600.0) * 16)

        # draw big pie
        qp.setPen(QtCore.Qt.NoPen)
        back_color = QtGui.QColor(self.color)
        back_color.setAlpha(100)
        no_back_color = QtGui.QColor(self.color)
        no_back_color.setAlpha(0)
        gradient = QtGui.QConicalGradient(
            0, 0, -30.0 * (past2h.hour + past2h.minute / 60.0)
        )
        gradient.setColorAt(5 / 6, back_color)
        gradient.setColorAt(1.0, no_back_color)
        back_brush = QtGui.QBrush(gradient)
        # back_brush.set
        qp.setBrush(back_brush)
        qp.drawPie(-cr, -cr, 2 * cr, 2 * cr, sangle, eangle)

        # draw small pie
        front_color = QtGui.QColor(self.color)
        front_color.setAlpha(200)
        gradient = QtGui.QConicalGradient(
            0, 0, -30.0 * (past2h.hour + past2h.minute / 60.0)
        )
        gradient.setColorAt(5 / 6, front_color)
        gradient.setColorAt(1.0, no_back_color)
        front_brush = QtGui.QBrush(gradient)
        qp.setBrush(front_brush)
        qp.drawPie(-cr + 20, -cr + 20, 2 * cr - 40, 2 * cr - 40, sangle, eangle)

        # cut out center disk
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_DestinationOut)
        qp.drawEllipse(-mr, -mr, 2 * mr, 2 * mr)
        qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)

        # draw duration arc
        if (
            self.duration >= dt.timedelta(minutes=30) and now < self.finish
        ):  # >= 30 minutes and not in the past
            arc_start = max(now, self.start)
            arc_end = self.finish
            arc_duration = arc_end - arc_start
            arc_true_duration = self.evt_finish - arc_start
            arc_sangle = -round(30.0 * (arc_start.hour + arc_start.minute / 60.0) * 16)
            arc_eangle = -round(30.0 * (arc_duration.total_seconds() / 3600.0) * 16)

            qp.save()
            arc_color = QtGui.QColor(self.color).darker()
            if arc_eangle + 5 * 16 < 0:
                arc_pen = QtGui.QPen(arc_color, 5)
                arc_pen.setCapStyle(QtCore.Qt.FlatCap)
                qp.setPen(arc_pen)
                qp.drawArc(
                    -cr + 25 + 7 * self.slot,
                    -cr + 25 + 7 * self.slot,
                    2 * cr - 50 - 14 * self.slot,
                    2 * cr - 50 - 14 * self.slot,
                    arc_sangle,
                    arc_eangle + 5 * 16,
                )

            # print duration text
            durangle = -arc_sangle / 16 + -arc_eangle / 16 - 1
            qp.rotate(durangle)
            font = QtGui.QFont("Raleway", 10 + FONT_ADJUST)
            font.setWeight(QtGui.QFont.Black)
            qp.setFont(font)
            dur_pen = QtGui.QPen(arc_color, 1)
            qp.setPen(dur_pen)

            duralign = QtCore.Qt.AlignRight
            # check if event on the left or right side of the clock face
            # and change direction if on the left side
            if 180 <= durangle % 360 < 360:
                qp.translate(cr - 23 - 7 * self.slot, -8)
                qp.rotate(180.0)
                duralign = QtCore.Qt.AlignLeft

            qp.drawText(
                0,
                -10,
                cr - 23 - 7 * self.slot,
                12,
                duralign,
                human_duration(arc_true_duration.total_seconds()),
            )
            qp.restore()

        # draw text
        if self.finish > past1h:
            qp.save()
            middle = self.start + (self.duration / 2)
            mangle = 30.0 * (middle.hour + middle.minute / 60.0)
            qp.rotate(mangle)

            # get text box width and height
            wangle = self.duration.total_seconds() / 120.0
            height = round(2 * (mr + 10) * math.sin(math.radians(wangle / 2))) + 10
            rect = QtCore.QRect(mr + 10, -height // 2, cr - mr - 40, height)

            # check if event on the left or right side of the clock face
            # and change direction if on the left side
            if 180 <= mangle % 360 < 360:
                qp.translate(cr + mr - 20, 0)
                qp.rotate(180.0)

            # use modified "Raleway" font with 70% line height from original
            # because Qt doesn't support changing line height (or I dunno how to do it)
            font = QtGui.QFont("Reallyway", 14 + FONT_ADJUST)
            qp.setFont(font)
            qp.setPen(QtGui.QPen(QtGui.QColor(theme("font")), 1))

            # check text boundaries, and adjust text alignment
            br = qp.boundingRect(rect, QtCore.Qt.TextWordWrap, self.text)
            align_flag = (
                QtCore.Qt.AlignHCenter
                if br.height() > height
                else QtCore.Qt.AlignCenter
            )

            # draw text finally
            qp.drawText(rect, align_flag | QtCore.Qt.TextWordWrap, self.text)
            qp.restore()

            # draw start time
            if self.evt_start >= past2h:
                qp.save()
                font = QtGui.QFont("Raleway", 12 + FONT_ADJUST)
                qp.setFont(font)

                stangle = 30.0 * (self.start.hour + self.start.minute / 60.0)
                qp.rotate(stangle)
                qp.translate(cr, 0)
                qp.rotate(97.0)

                align = QtCore.Qt.AlignLeft
                if 120 <= stangle % 360 <= 240:
                    qp.translate(40, 20)
                    qp.rotate(180.0)
                    align = QtCore.Qt.AlignRight

                qp.setPen(QtGui.QPen(QtGui.QColor(theme("font")), 1))
                qp.drawText(
                    0,
                    0,
                    35,
                    20,
                    align | QtCore.Qt.AlignVCenter,
                    "  " + time(self.evt_start),
                )
                qp.restore()

            # draw finish time
            if self.duration >= dt.timedelta(hours=1):
                qp.save()
                font = QtGui.QFont("Raleway", 12 + FONT_ADJUST)
                qp.setFont(font)

                etangle = 30.0 * (self.finish.hour + self.finish.minute / 60.0)
                qp.rotate(etangle)
                qp.translate(cr, 0)
                qp.rotate(83.0)

                align = QtCore.Qt.AlignRight
                if 120 <= etangle % 360 <= 240:
                    qp.translate(-45, 20)
                    qp.rotate(180.0)
                    align = QtCore.Qt.AlignLeft

                qp.setPen(QtGui.QPen(QtGui.QColor(theme("font")), 1))
                qp.drawText(
                    -40,
                    0,
                    35,
                    20,
                    align | QtCore.Qt.AlignVCenter,
                    time(self.evt_finish),
                )
                qp.restore()
