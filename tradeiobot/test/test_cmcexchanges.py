import os
import requests
from bs4 import BeautifulSoup
from unittest.mock import MagicMock
from tradeiobot.util import dotdict


def setup_module():
    os.environ["TELEGRAM_TOKEN"] = "t0ken"
    with open('./tradeiobot/test/data_cmcexchanges.html') as f:
        mock = MagicMock(return_value=dotdict(dict(content=f.read())))
        requests.get = mock

def teardown_module():
    os.environ["TELEGRAM_TOKEN"] = ""

def test_load_howsitcoming_soup():
    from tradeiobot.config import CMC_EXCHANGEVOLUMES_URL
    from tradeiobot.scrapers.cmc import _load_exchangevolumes_soup
    soup = _load_exchangevolumes_soup()
    requests.get.assert_called_once_with(CMC_EXCHANGEVOLUMES_URL)
    assert isinstance(soup, BeautifulSoup)

def test_load_cmc_data():
    from tradeiobot.scrapers.cmc import load_cmc_data
    data = load_cmc_data()
    assert data == {'rank': '119', 'volume': 693282.218976}

