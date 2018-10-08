import os
from unittest.mock import MagicMock

def setup_module():
    os.environ["TELEGRAM_TOKEN"] = "t0ken"

def teardown_module():
    os.environ["TELEGRAM_TOKEN"] = ""

def test_load_marketdata():
    import tradeiobot.api.tradeio
    import requests
    from tradeiobot.config import API_TRADEIO_ENDPOINT

    mock = MagicMock()
    requests.get = mock
    tradeiobot.api.tradeio.load_marketdata()
    mock.assert_called_once_with(API_TRADEIO_ENDPOINT)

def test_load_token_ticker():
    import tradeiobot.api.cmc
    import requests
    from tradeiobot.config import API_CMC_ENDPOINT

    mock = MagicMock()
    requests.get = mock
    tradeiobot.api.cmc.load_token_ticker()
    mock.assert_called_once_with(API_CMC_ENDPOINT)
