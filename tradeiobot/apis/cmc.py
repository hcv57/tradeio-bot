import requests
import tradeiobot.config
from tradeiobot.cache import cache

@cache("API_CMC", tradeiobot.config.API_CMC_CACHE_FOR_SECONDS)
def load_token_ticker():
    return requests.get(tradeiobot.config.API_CMC_ENDPOINT).json()