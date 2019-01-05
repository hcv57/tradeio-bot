from functools import partial

from tradeiobot.db.stores import memory, sqlite
from tradeiobot.db.stores.abstractstore import AbstractStore

def connect(drivers=[]):

    class Connection(object):

        def __init__(self, stores):
            self.stores = stores or [memory, sqlite]
            assert all(lambda s: isinstance(s, AbstractStore) for s in self.stores)

        def __getattr__(self, item):

            def noop(*args, **kwargs):
                pass

            func = noop

            for store in reversed(object.__getattribute__(self, "stores")):
                action = store.__getattribute__(item)
                assert callable(action)
                func = partial(action, next_store_action=func)

            return func

    return Connection(drivers)


connection = connect()