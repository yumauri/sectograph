from sectograph import database, entities


class BaseEvent:
    db: database.Database

    def __init__(self, db: database.Database) -> None:
        self.db = db

    def add(self, e: entities.BaseEvent) -> None:
        con = self.db.con
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO events(start, finish, text, color, notify, sound, day, repeat, end)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                e.start,
                e.finish,
                e.text,
                e.color,
                e.notify,
                e.sound,
                e.day,
                e.repeat,
                e.end,
            ),
        )
        con.commit()
        e.id = cur.lastrowid

    def update(self, e: entities.BaseEvent) -> None:
        con = self.db.con
        cur = con.cursor()
        cur.execute(
            """
            UPDATE events
            SET start = ?, finish = ?, text = ?, color = ?, notify = ?, sound = ?, day = ?, repeat = ?, end = ?
            WHERE id = ?
        """,
            (
                e.start,
                e.finish,
                e.text,
                e.color,
                e.notify,
                e.sound,
                e.day,
                e.repeat,
                e.end,
                e.id,
            ),
        )
        con.commit()

    def delete(self, e: entities.BaseEvent) -> None:
        con = self.db.con
        cur = con.cursor()
        cur.execute(
            """
            DELETE from events
            WHERE id = ?
        """,
            (e.id,),
        )
        con.commit()
