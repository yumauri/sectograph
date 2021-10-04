from __future__ import annotations
from sectograph import database


class Color:
    db: database.Database

    def __init__(self, db: database.Database) -> None:
        self.db = db

    def get(self) -> list[str]:
        con = self.db.con
        cur = con.cursor()
        result = cur.execute(
            """
            SELECT name
            FROM colors
        """
        ).fetchall()
        return [row["name"] for row in result]
