import tradeiobot.config as config
from telegram.ext import Updater, CommandHandler
from tradeiobot.markets import get_total_volume

# import logging
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO)


def volume(bot, update):
    total_volume = get_total_volume()
    update.message.reply_text(
        "{:,.2f} USDT".format(total_volume)
    )

def start():
    updater = Updater(config.TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('volume', volume))
    updater.start_polling()
    updater.idle()