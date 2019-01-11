import tradeiobot.bot.handlers
from tradeiobot.config import VERSION
from tradeiobot.db import connection
from distutils.version import LooseVersion

def showonce(handler):
    "decorator for telegram bot handlers"

    def wrapper(*args, **kwargs):
        global users
        user = args[1].message.from_user.id
        known_release = connection.get("user_release", user) or "0"
        if LooseVersion(VERSION) > LooseVersion(known_release):
            _handler = tradeiobot.bot.handlers.releasenotes_handler
            connection.set("user_release", user, VERSION)
        else:
            _handler = handler
        return _handler(*args, **kwargs)

    return wrapper


