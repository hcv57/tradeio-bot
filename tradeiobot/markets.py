import tradeiobot.apis.tradeio
import tradeiobot.config


def get_instruments():
    data = tradeiobot.apis.tradeio.load_marketdata()
    return {d["instrument"].upper(): d for d in data}


def get_instrument(instrument_name, enrich=False):
    instrument = get_instruments().get(instrument_name, {})
    from_, to = instrument_name.split("_")
    enriched_instrument = dict(instrument)
    if enrich:
        for k, v in instrument.items():
            if k in ["open", "close", "high", "low"]:
                key = "{}_usdt".format(k)
                enriched_instrument[key] = convert_currency(v, to, "USDT")
        enriched_instrument["volume_usdt"] = convert_currency(
            instrument["volume"] * instrument["close"],
            to,
            "USDT"
        )
    return enriched_instrument


def get_exchange_volumes():
    volumes = dict(BTC=0, ETH=0, TIOX=0, USDT=0, TUSD=0, EUR=0, GBP=0)
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
        try:
            return amount / instrument["close"]
        except ZeroDivisionError:
            return 0
