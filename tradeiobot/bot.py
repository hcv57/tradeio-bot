import tradeiobot.config as config
from telegram.ext import Updater, CommandHandler

updater = Updater(config.TELEGRAM_TOKEN)

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

updater.dispatcher.add_handler(CommandHandler('hello', hello))

def start():
    updater.start_polling()
    updater.idle()