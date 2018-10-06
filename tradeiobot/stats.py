import time

#FIXME these stats are likely off. find out how the telegram bot lib actually runs (i.e. multiple threads?)


hits = 0
users = set()
running_since = time.time()

def track(handler):
    "decorator for telegram bot handlers"

    def wrapper(*args, **kwargs):
        global hits
        global users
        hits += 1
        users.add(args[1].message.from_user.id)
        return handler(*args, **kwargs)
    return wrapper

def get_hits():
    return hits

def get_unique_users():
    return len(users)

def get_uptime():
    return int(time.time() - running_since)