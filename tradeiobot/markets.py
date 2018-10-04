import json
import tradeiobot.api
import tradeiobot.config
from tradeiobot.cache import cache

def load_marketdata():
    return json.loads(tradeiobot.api.load_marketdata())

@cache("MARKETDATA", tradeiobot.config.CACHE_FOR_SECONDS)
def get_instruments():
    data = load_marketdata()
    return {d["instrument"].upper() : d for d in data}

def get_instrument(instrument):
    return get_instruments().get(instrument, {})

def get_exchange_volumes():
    volumes = dict(BTC=0, ETH=0, TIO=0, USDT=0)
    for k, v in get_instruments().items():
        currency = k.split("_")[1]
        volumes[currency] += v.get("volume") * v.get("close")
    return volumes

def get_total_volume(currency="USDT"):
    total = 0
    for k, v in get_exchange_volumes().items():
        total += convert_currency(v, k, currency)
    return total

def convert_currency(amount, from_, to):
    if from_ == to:
        return amount
    try:
        instrument_name = from_ + "_" + to
        instrument = get_instrument(instrument_name)
        return amount * instrument["close"]
    except KeyError:
        instrument_name = to + "_" + from_
        instrument = get_instrument(instrument_name)
        return amount / instrument["close"]
