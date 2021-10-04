from sectograph import datetime as dt
from .entity import Entity


class BaseEvent(Entity):
    start: dt.datetime
    finish: dt.datetime
    text: str
    color: str
    notify: int
    sound: str
    day: bool
    repeat: int
    end: dt.datetime

    def __init__(
        self,
        *,
        id: int = None,
        start: dt.datetime,
        finish: dt.datetime,
        text: str,
        color: str,
        notify: int = None,
        sound: str = None,
        day: bool = False,
        repeat: int = None,
        end: dt.date = None,
    ):
        if end:
            end = dt.datetime.combine(end, dt.app_time()) if repeat else None
        super().__init__(id)
        self.start = start
        self.finish = finish
        self.text = text
        self.color = color
        self.notify = notify
        self.sound = sound
        self.day = day
        self.repeat = repeat
        self.end = end
