import requests
import tradeiobot.config
from tradeiobot.cache import cache

@cache("API_TRADEIO", tradeiobot.config.API_TRADEIO_CACHE_FOR_SECONDS)
def load_marketdata():
    return requests.get(tradeiobot.config.API_TRADEIO_ENDPOINT).json()