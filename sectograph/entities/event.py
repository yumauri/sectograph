from sectograph import datetime as dt
from .base_event import BaseEvent


class Event(BaseEvent):
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
        repeat: int = None,
        end: dt.date = None,
    ):
        super().__init__(
            id=id,
            start=start,
            finish=finish,
            text=text,
            color=color,
            notify=notify,
            sound=sound,
            day=False,
            repeat=repeat,
            end=end,
        )

    @classmethod
    def from_base_event(cls, e: BaseEvent):
        return cls(
            id=e.id,
            start=e.start,
            finish=e.finish,
            text=e.text,
            color=e.color,
            notify=e.notify,
            sound=e.sound,
            repeat=e.repeat,
            end=e.end,
        )
