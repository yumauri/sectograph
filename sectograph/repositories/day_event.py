from __future__ import annotations
from sectograph import entities, datetime as dt
from .base_event import BaseEvent


class DayEvent(BaseEvent):
    def get(self) -> list[entities.DayEvent]:
        now = dt.app_now()
        con = self.db.con
        cur = con.cursor()
        result = cur.execute(
            """
            SELECT id, start, text, color, notify, sound, repeat, end
            FROM events
            WHERE day == 1 AND ((
                repeat IS NULL
                AND DATE(start) == DATE(?)
            ) OR (
                repeat IS NOT NULL
                AND (end IS NULL OR end >= DATE(?))
                AND CAST(JULIANDAY(?) - JULIANDAY(start) AS INT) % repeat = 0
            ))
            ORDER BY id
        """,
            (now, now, now),
        ).fetchall()
        return [entities.DayEvent(**row) for row in result]
