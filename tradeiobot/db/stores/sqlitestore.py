import sqlite3
import threading

import tradeiobot.config
from tradeiobot.db.stores.abstractstore import AbstractStore


class SqliteStore(AbstractStore):

    def __init__(self, memory=False):
        self.rlock = threading.RLock()

        self.connection = sqlite3.connect(
            ":memory:" if memory else tradeiobot.config.SQLITE_DB,
            check_same_thread=False
        )
        self._create_table()

    def _create_table(self):
        with self.rlock:
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS store(t text, k text, v text, PRIMARY KEY(t, k))"
            )
            self.connection.commit()

    def do_get(self, table, key):
        result = self.connection.execute(
            "SELECT v FROM store WHERE t=? AND k=?",
            (table, key)
        ).fetchone()
        return result[0] if result else result

    def do_get_all_as_dict(self, table):
        return dict(self.connection.execute(
            "SELECT k, v FROM store WHERE t=?",
            (table,)
        ))

    def do_set(self, table, key, value):
        with self.rlock:
            self.connection.execute(
                "INSERT OR REPLACE INTO store(t, k, v) VALUES (?, ?, ?)",
                (table, key, value)
            )
            self.connection.commit()

    def do_delete(self, table, key):
        with self.rlock:
            self.connection.execute(
                "DELETE FROM store WHERE t=? AND k=?",
                (table, key)
            )
            self.connection.commit()


store = SqliteStore()
