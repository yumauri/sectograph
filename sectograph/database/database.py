import sqlite3


class Database:
    con: sqlite3.Connection

    def __init__(self):
        self.con = sqlite3.connect(
            "sectograph/database/db.sqlite",
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        sqlite3.register_adapter(bool, int)
        sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
        self.con.row_factory = sqlite3.Row

    def close(self):
        self.con.close()
