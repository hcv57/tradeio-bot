import json
import sqlite3
import tradeiobot.config
from tradeiobot.db.stores.abstractstore import AbstractStore


class SqliteStore(AbstractStore):

    def __init__(self, memory=False):
        db = ":memory:" if memory else tradeiobot.config.SQLITE_DB
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS store(t text, k text, v text, PRIMARY KEY(t, k))"
        )
        self.connection.commit()

    def do_get(self, table, key):
        return self.cursor.execute(
            "SELECT v FROM store WHERE t=? AND k=?",
            (table, key)
        )

    def do_get_all_as_dict(self, table):
        return dict(self.cursor.execute(
            "SELECT k, v FROM store WHERE t=?",
            (table, )
        ))

    def do_set(self, table, key, value):
        self.cursor.execute(
            "INSERT OR REPLACE INTO store(t, k, v) VALUES (?, ?, ?)",
            (table, key, value)
        )
        self.connection.commit()

    def do_delete(self, table, key):
        self.cursor.execute(
            "DELETE FROM store WHERE t=? AND k=?",
            (table, key)
        )
        self.connection.commit()


store = SqliteStore()