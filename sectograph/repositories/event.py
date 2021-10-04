from __future__ import annotations
from sectograph import entities, datetime as dt
from .base_event import BaseEvent


class Event(BaseEvent):
    def get(self) -> list[entities.Event]:
        now = dt.app_now()
        con = self.db.con
        cur = con.cursor()
        result = cur.execute(
            """
            SELECT id, start, finish, text, color, notify, sound, repeat, end
            FROM events
            WHERE day != 1 AND ((
                repeat IS NULL
                AND finish > DATETIME(?, '-2 hours')
                AND start < DATETIME(?, '+11 hours')
            ) OR (
                repeat IS NOT NULL
                AND (end IS NULL OR end >= DATE(?))
                AND CAST((JULIANDAY(DATE(?)) - JULIANDAY(DATE(start))) AS INT) % repeat = 0
                AND DATETIME(DATE(?), TIME(finish)) > DATETIME(?, '-2 hours')
                AND DATETIME(DATE(?), TIME(start)) < DATETIME(?, '+11 hours')
            ))
            ORDER BY TIME(start)
        """,
            (now, now, now, now, now, now, now, now),
        ).fetchall()
        return [entities.Event(**row) for row in result]

    def get_minute_alerts(self):
        now = dt.app_now()
        con = self.db.con
        cur = con.cursor()
        result = cur.execute(
            """
            SELECT
                CASE WHEN mod IS NULL THEN start_time ELSE now_start_time END AS "time [timestamp]",
                text,
                sound
            FROM (
                SELECT
                  start,
                  DATETIME(DATE(?), TIME(start)) as now_start,
                  CAST((JULIANDAY(DATE(?)) - JULIANDAY(DATE(start))) AS INT) % repeat as mod,
                  DATETIME(start, "-" || notify || " minutes") as start_time,
                  DATETIME(DATE(?), TIME(start), "-" || notify || " minutes") as now_start_time,
                  *
                FROM events
                WHERE notify IS NOT NULL
                AND (mod == 0 OR mod IS NULL)
            )
            WHERE "time [timestamp]" >= DATETIME(?)
            AND "time [timestamp]" < DATETIME(?, '+1 minute')
            """,
            (now, now, now, now, now),
        ).fetchall()
        return [dict(row) for row in result]
