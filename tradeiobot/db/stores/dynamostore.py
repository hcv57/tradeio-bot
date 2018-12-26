from tradeiobot.db.stores.abstractstore import AbstractStore

class DynamoStore(AbstractStore):

    def __init__(self):
        self.store = {}

    def set(self, key, value, next_store=None):
        self.store[key] = value

    def get(self, key, next_store=None):
        return self.store.get(key)

store = DynamoStore()