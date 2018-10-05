import requests
import tradeiobot.config
from tradeiobot.cache import cache

@cache("API", tradeiobot.config.CACHE_FOR_SECONDS)
def load_marketdata():
    return requests.get(tradeiobot.config.API_ENDPOINT).json()