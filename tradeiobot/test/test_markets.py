import os
import json

def setup_module():
    os.environ["TELEGRAM_TOKEN"] = "t0ken"
    import tradeiobot.apis.tradeio
    tradeiobot.apis.tradeio.load_marketdata = lambda: json.loads(load_test_data())

def teardown_module():
    os.environ["TELEGRAM_TOKEN"] = ""

def load_test_data():
    with open('./tradeiobot/test/data_tradeio_market.json') as f:
        return f.read()


def test_get_instruments():
    from tradeiobot.markets import get_instruments
    instruments = get_instruments()
    assert len(instruments.keys()) == 47


def test_get_instrument():
    from tradeiobot.markets import get_instrument
    instrument = get_instrument("LTC_BTC")
    assert instrument["low"] == 0.00774255


def test_get_exchange_volumes():
    from tradeiobot.markets import get_exchange_volumes
    volumes = get_exchange_volumes()
    # FIXME rounding errors using floats for currency
    assert int(volumes["BTC"]) == 6
    assert int(volumes["ETH"]) == 282
    assert int(volumes["TIOX"]) == 423052
    assert int(volumes["USDT"]) == 94830


def test_get_total_volume():
    from tradeiobot.markets import get_total_volume
    # FIXME rounding errors using floats for currency
    assert get_total_volume() == get_total_volume("USDT")
    assert int(get_total_volume()) == 298916
    assert int(get_total_volume("BTC")) == 45
    assert int(get_total_volume("ETH")) == 1423
    assert int(get_total_volume("TIOX")) == 1240373
