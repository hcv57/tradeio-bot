import os
import json

def setup_module():
    os.environ["TELEGRAM_TOKEN"] = "t0ken"
    import tradeiobot.api.cmc
    tradeiobot.api.cmc.load_token_ticker = lambda: json.loads(load_test_data())

def teardown_module():
    os.environ["TELEGRAM_TOKEN"] = ""

def load_test_data():
    with open('./tradeiobot/test/data_cmc_ticker.json') as f:
        return f.read()

def test_load_token_ticker():
    import tradeiobot.token
    ticker = tradeiobot.token.load_token_ticker()
    assert ticker["name"] == "Trade Token"
    assert ticker["rank"]  == 245
    assert ticker["circulating_supply"] == 89921436.0
    assert ticker["total_supply"] == 223534823.0
    assert ticker["price_usd"] == 0.1831727524
    assert ticker["volume_24h_usd"] == 34985.2977132928
    assert ticker["market_cap_usd"] == 16471157.0
