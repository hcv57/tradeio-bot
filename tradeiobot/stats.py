import time
from tradeiobot.db import connection


running_since = time.time()

def track(handler):
    "decorator for telegram bot handlers"

    def wrapper(*args, **kwargs):
        total_hits = int(connection.get("stats", "total_hits") or 0)
        connection.set("stats", "total_hits", total_hits + 1)

        user = args[1].message.from_user.id
        user_hits = int(connection.get("user_hits", user) or 0)
        connection.set("user_hits", user, user_hits + 1)
        return handler(*args, **kwargs)
    return wrapper

def get_hits():
    return int(connection.get("stats", "total_hits") or 0)

def get_unique_users():
    return len(connection.get_all_as_dict("user_hits"))

def get_uptime():
    return int(time.time() - running_since)