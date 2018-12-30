import abc


class AbstractStore(abc.ABC):

    def get(self, key, next_store_action):
        value = self.do_get(key)
        if not value:
            value = next_store_action(key)
            if value: # then update the local store
                self.do_set(key, value)
        return value

    def set(self, key, value, next_store_action):
        self.do_set(key, value)
        next_store_action(key, value)

    def delete(self, key, next_store_action):
        self.do_delete(key)
        next_store_action(key)

    @abc.abstractmethod
    def do_get(self, key):
        pass

    @abc.abstractmethod
    def do_set(self, key, value):
        pass

    @abc.abstractmethod
    def do_delete(self, key):
        pass