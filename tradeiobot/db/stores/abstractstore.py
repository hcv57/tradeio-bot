import abc


class AbstractStore(abc.ABC):

    def get(self, table, key, next_store_action):
        value = self.do_get(table, key)
        if not value:
            value = next_store_action(table, key)
            if value: # then update the local store
                self.do_set(table, key, value)
        return value

    def get_all_as_dict(self, table, next_store_action):
        values = self.do_get_all_as_dict(table)
        if not values:
            values = next_store_action(table)
            for k, v in values:
                self.do_set(table, k, v)
        return values

    def set(self, table, key, value, next_store_action):
        self.do_set(table, key, value)
        next_store_action(table, key, value)

    def delete(self, table, key, next_store_action):
        self.do_delete(table, key)
        next_store_action(table, key)

    @abc.abstractmethod
    def do_get(self, table, key):
        pass

    @abc.abstractmethod
    def do_get_all_as_dict(self, table):
        pass

    @abc.abstractmethod
    def do_set(self, table, key, value):
        pass

    @abc.abstractmethod
    def do_delete(self, table, key):
        pass