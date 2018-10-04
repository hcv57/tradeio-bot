import time
from collections import namedtuple


def cache(key, expiry):
    "Cache decorator"

    def decorate(f):
        store = dict()
        def wrapped(*args, **kwargs):
            now = int(time.time()) # seconds since epoch
            item = store.get(key, {})
            if item.get("timestamp", 0) < now - expiry:
                # expired
                item["timestamp"] = now
                item["value"] = f(*args, **kwargs)
                store[key] = item
            return item["value"]
        return wrapped
    return decorate