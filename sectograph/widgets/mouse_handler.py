from __future__ import annotations
import math
import functools
from PyQt5 import QtCore, QtGui, QtWidgets
from sectograph import entities, widgets, datetime as dt


class MouseHandler(QtWidgets.QWidget):
    app: widgets.Application
    events: list[entities.Event]
    day_events: list[entities.DayEvent]

    def __init__(self, parent: QtWidgets.QWidget, app: widgets.Application):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.app = app
        self.menu = QtWidgets.QMenu(self)

    def update_events(
        self, events: list[entities.Event], day_events: list[entities.DayEvent]
    ):
        self.events = events
        self.day_events = day_events

    def get_events_by_coords(self, x: int, y: int) -> list[entities.BaseEvent]:
        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        r = min(cx, cy)
        dx, dy = x - cx, y - cy
        dr = (dx ** 2 + dy ** 2) ** 0.5
        angle = math.degrees(math.acos(-dy / dr)) if dr != 0 else 0
        if dx < 0:
            angle = 360.0 - angle

        # clock_r = 0, 40
        sector_r = 45, r - 20
        day_r = r - 20, r

        # if click was happen inside sectors area
        if sector_r[0] < dr < sector_r[1]:
            now = dt.app_now()
            past2h = now - dt.timedelta(hours=2)
            future10h = now + dt.timedelta(hours=10)

            h = angle / 30
            time = dt.time(hour=int(h), minute=int(60 * (h % 1)))
            on = []
            for ev in self.events:
                # adjust date for repeated events
                if ev.repeat:
                    astart = ev.start.replace(
                        year=now.year, month=now.month, day=now.day
                    )
                    afinish = ev.finish.replace(
                        year=now.year, month=now.month, day=now.day
                    )
                    afinish += ev.finish.date() - ev.start.date()
                else:
                    astart = ev.start
                    afinish = ev.finish

                estart = max(past2h, astart)
                efinish = min(future10h, afinish)
                start = dt.time(hour=int(estart.strftime("%I")), minute=estart.minute)
                if start.hour == 12:
                    start = start.replace(hour=0)
                finish = dt.time(
                    hour=int(efinish.strftime("%I")), minute=efinish.minute
                )
                if start <= time <= finish:
                    on.append(ev)
            return on

        # if click was happen inside day events area (outer circle)
        if day_r[0] < dr < day_r[1]:
            idx = int(angle / 30)
            if idx < len(self.day_events):
                return [self.day_events[idx]]
            return []

        # if click was happen outside or inside clock // TODO redo later
        return []

    def mouseMoveEvent(self, event):
        if self.get_events_by_coords(event.x(), event.y()):
            self.setCursor(QtCore.Qt.PointingHandCursor)
        elif self.cursor() == QtCore.Qt.PointingHandCursor:
            self.unsetCursor()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        x, y = event.x(), event.y()
        on = self.get_events_by_coords(x, y)
        if on:
            self.menu.clear()
            for ev in on:
                action = QtWidgets.QAction(ev.text, self.menu)
                action.triggered.connect(functools.partial(self.open_edit_window, ev))
                self.menu.addAction(action)
            self.menu.move(QtGui.QCursor.pos())
            self.menu.show()

    def open_edit_window(self, evt: entities.BaseEvent):
        self.app.edit_window.open(evt)
