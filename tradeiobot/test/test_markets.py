import os
import json

def setup_module():
    os.environ["TELEGRAM_TOKEN"] = "t0ken"
    import tradeiobot.api.tradeio
    tradeiobot.api.tradeio.load_marketdata = lambda: json.loads(load_test_data())

def teardown_module():
    os.environ["TELEGRAM_TOKEN"] = ""

def load_test_data():
    with open('./tradeiobot/test/data_tradeio_market.json') as f:
        return f.read()


def test_get_instruments():
    from tradeiobot.markets import get_instruments
    instruments = get_instruments()
    assert len(instruments.keys()) == 35


def test_get_instrument():
    from tradeiobot.markets import get_instrument
    instrument = get_instrument("LTC_BTC")
    assert instrument["low"] == 0.00879323


def test_get_exchange_volumes():
    from tradeiobot.markets import get_exchange_volumes
    volumes = get_exchange_volumes()
    # FIXME rounding errors using floats for currency
    assert int(volumes["BTC"]) == 9
    assert int(volumes["ETH"]) == 173
    assert int(volumes["TIO"]) == 354420
    assert int(volumes["USDT"]) == 106295


def test_get_total_volume():
    from tradeiobot.markets import get_total_volume
    # FIXME rounding errors using floats for currency
    assert get_total_volume() == get_total_volume("USDT")
    assert int(get_total_volume()) == 269661
    assert int(get_total_volume("BTC")) == 40
    assert int(get_total_volume("ETH")) == 1202
    assert int(get_total_volume("TIO")) == 1530670
