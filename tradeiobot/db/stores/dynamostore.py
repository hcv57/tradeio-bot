from tradeiobot.db.stores.abstractstore import AbstractStore


class DynamoStore(AbstractStore):

    def __init__(self):
        self.store = {}

    def do_get(self, key):
        return self.store.get(key)

    def do_set(self, key, value):
        self.store[key] = value
        return True

    def do_delete(self, key):
        del self.store[key]
        return True

store = DynamoStore()