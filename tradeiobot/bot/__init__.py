import tradeiobot.config
import tradeiobot.bot.handlers

from telegram.ext import Updater, CommandHandler, RegexHandler



def start():
    handlers = [
        CommandHandler('start', tradeiobot.bot.handlers.start_handler),
        CommandHandler('markets', tradeiobot.bot.handlers.markets_handler),
        CommandHandler('volume', tradeiobot.bot.handlers.volume_handler),
        CommandHandler('exchange', tradeiobot.bot.handlers.exchange_handler),
        CommandHandler('token', tradeiobot.bot.handlers.token_handler),
        CommandHandler('about', tradeiobot.bot.handlers.about_handler),
        CommandHandler('progress', tradeiobot.bot.handlers.progress_handler),
        RegexHandler('/([A-Z]+_[A-Z]+)', tradeiobot.bot.handlers.instrument_handler, pass_groups=True),
    ]

    updater = Updater(tradeiobot.config.TELEGRAM_TOKEN)
    for h in handlers:
        updater.dispatcher.add_handler(h)
    updater.start_polling()
    updater.idle()
