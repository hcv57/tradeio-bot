import os
from unittest.mock import MagicMock

def setup_module():
    os.environ["TELEGRAM_TOKEN"] = "t0ken"

def teardown_module():
    os.environ["TELEGRAM_TOKEN"] = ""

def test_load_marketdata():
    import tradeiobot.api
    import requests
    from tradeiobot.config import API_ENDPOINT

    mock = MagicMock()
    requests.get = mock
    tradeiobot.api.load_marketdata()
    mock.assert_called_once_with(API_ENDPOINT)