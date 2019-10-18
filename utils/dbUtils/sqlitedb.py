from utils.dbUtils.DB import DB
import sqlite3


class SqliteDB(DB):
    def __init__(self, db):
        self.db = db
        pass

    def conn(self):
        self.con = sqlite3.connect(self.db)
        return self.con
        pass


