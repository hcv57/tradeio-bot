class AbstractStore(object):

    def get(key, next_store=None):
        raise NotImplementedError

    def set(key, value, next_store=None):
        raise NotImplementedError

    def delete(key, next_store=None):
        raise NotImplementedError