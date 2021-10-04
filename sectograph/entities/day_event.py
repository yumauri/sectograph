from sectograph import datetime as dt
from .base_event import BaseEvent


class DayEvent(BaseEvent):
    def __init__(
        self,
        *,
        id: int = None,
        start: dt.date,
        text: str,
        color: str,
        notify: int = None,
        sound: str = None,
        repeat: int = None,
        end: dt.date = None,
    ):
        start = dt.datetime.combine(start, dt.app_time())
        super().__init__(
            id=id,
            start=start,
            finish=start,
            text=text,
            color=color,
            notify=notify,
            sound=sound,
            day=True,
            repeat=repeat,
            end=end,
        )

    @classmethod
    def from_base_event(cls, e: BaseEvent):
        start = dt.datetime.combine(e.start.date(), dt.app_time())
        return cls(
            id=e.id,
            start=start,
            text=e.text,
            color=e.color,
            notify=e.notify,
            sound=e.sound,
            repeat=e.repeat,
            end=e.end,
        )
