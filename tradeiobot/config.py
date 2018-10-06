import os
import subprocess
import binascii

API_ENDPOINT = 'https://api.exchange.trade.io/marketdata-ws/24hr'
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CACHE_FOR_SECONDS = 60
SPONSOR_MESSAGE = "\nBrought to you by coinrank.chat\n_Cryptocurrency projects ranked by Telegram chats_"

try:
    COMMIT = subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD']
    ).decode('UTF-8').strip()
except:
    COMMIT = "git command unavailable"

if not TELEGRAM_TOKEN:
    raise ValueError('The environment variable TELEGRAM_TOKEN is not set.')