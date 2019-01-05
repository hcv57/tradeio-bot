from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    # http://unicode.org/emoji/charts/full-emoji-list.html
    return ReplyKeyboardMarkup([
        [KeyboardButton('/balance (beta)')],
        [KeyboardButton('/markets 📈'), KeyboardButton('/volume 💰'), KeyboardButton('/exchange 🚀')],
        [KeyboardButton('/token 💎'), KeyboardButton('/progress 🚦'),  KeyboardButton('/about ℹ')]
    ], resize_keyboard=True)