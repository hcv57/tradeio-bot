import os
import subprocess
import binascii

# Telegram
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError('The environment variable TELEGRAM_TOKEN is not set.')

# API Endpoints
API_CMC_TIO_ID = "2373"
API_CMC_ENDPOINT = "https://api.coinmarketcap.com/v2/ticker/{}/".format(API_CMC_TIO_ID)
API_TRADEIO_ENDPOINT = "https://api.exchange.trade.io/marketdata-ws/24hr"

# Cache config
API_TRADEIO_CACHE_FOR_SECONDS = 60
API_CMC_CACHE_FOR_SECONDS = 180

# git commit hash
try:
    COMMIT = subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD']
    ).decode('UTF-8').strip()
except:
    COMMIT = "git command unavailable"

# Sponsor
SPONSOR_MESSAGE = "\nBrought to you by coinrank.chat\n_Cryptocurrency projects ranked by Telegram chats_"
