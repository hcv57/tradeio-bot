import os

API_ENDPOINT = 'https://api.exchange.trade.io/marketdata-ws/24hr'
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CACHE_FOR_SECONDS = 60
SPONSOR_MESSAGE = "\nBrought to you by coinrank.chat\n_Cryptocurrency projects ranked by Telegram chats_"

if not TELEGRAM_TOKEN:
    raise ValueError('The environment variable TELEGRAM_TOKEN is not set.')