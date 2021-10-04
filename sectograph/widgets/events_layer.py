from __future__ import annotations
from PyQt5 import QtCore, QtGui, QtWidgets
from sectograph import widgets, resources, entities


class EventsLayer(QtWidgets.QWidget):
    events: list[widgets.Event]
    day_events: list[widgets.DayEvent]

    def __init__(
        self, parent: QtWidgets.QWidget, theme: resources.Theme, theme_name: str
    ) -> None:
        super().__init__(parent)
        self.theme = theme
        self.theme_name = theme_name
        self.events = []
        self.day_events = []

    def re_slot_events(self):
        resorted_events = sorted(self.events, key=lambda e: e.finish, reverse=True)
        all_re_slotted = False
        while not all_re_slotted:
            all_re_slotted = True
            for i in range(len(resorted_events)):
                for j in range(len(resorted_events)):
                    if i != j:
                        current = resorted_events[i]
                        compare = resorted_events[j]
                        if (
                            compare.start < current.finish < compare.finish
                            and current.slot == compare.slot
                        ):
                            current.slot = compare.slot + 1
                            all_re_slotted = False

    def update_events(
        self, events: list[entities.Event], day_events: list[entities.DayEvent]
    ) -> None:
        # to update events we remove all of them and adds anew
        # I guess this is not good for performance,
        # but for educational project will do the trick

        # remove all old widgets
        for ev in [*self.events, *self.day_events]:
            ev.setParent(None)  # set parent to None, so GC should remove objects

        # create new widgets
        self.events = [
            widgets.Event(self, self.theme, self.theme_name, ev)
            for ev in sorted(events, key=lambda e: e.finish - e.start, reverse=True)
        ]
        self.day_events = [
            widgets.DayEvent(self, self.theme, self.theme_name, ev, i)
            for i, ev in enumerate(day_events)
        ]

        # update widgets' slots
        self.re_slot_events()

        # trigger resizeEvent manually to set all child events geometry
        self.resizeEvent(QtGui.QResizeEvent(self.size(), QtCore.QSize()))

        # show all events
        for ev in [*self.events, *self.day_events]:
            ev.show()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        full = self.rect()
        small = QtCore.QRect(20, 20, self.width() - 40, self.height() - 40)
        # resize all children widgets
        for ev in self.events:
            ev.setGeometry(small)
        for ev in self.day_events:
            ev.setGeometry(full)
