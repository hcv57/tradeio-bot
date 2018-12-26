users = set()

def showonce(handler):
    "decorator for telegram bot handlers"

    def wrapper(*args, **kwargs):
        global users
        user = args[1].message.from_user.id
        if user in users:
            _handler = handler
        else:
            users.add(user)
            _handler = releasenotes_handler
        return _handler(*args, **kwargs)

    return wrapper


def releasenotes_handler(bot, update):
    with open("RELEASES") as f:
        update.message.reply_markdown(
            "*What's new?*\n\n" +
            f.read()
        )

