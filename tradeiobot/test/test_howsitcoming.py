import os
import requests
from bs4 import BeautifulSoup
from unittest.mock import MagicMock
from tradeiobot.util import dotdict


def setup_module():
    os.environ["TELEGRAM_TOKEN"] = "t0ken"
    with open('./tradeiobot/test/data_howsitcoming.html') as f:
        mock = MagicMock(return_value=dotdict(dict(content=f.read())))
        requests.get = mock

def teardown_module():
    os.environ["TELEGRAM_TOKEN"] = ""

def test_load_howsitcoming_soup():
    from tradeiobot.config import HOWSITCOMING_URL
    from tradeiobot.scrapers.howsitcoming import _load_howsitcoming_soup
    soup = _load_howsitcoming_soup()
    requests.get.assert_called_once_with(HOWSITCOMING_URL)
    assert isinstance(soup, BeautifulSoup)

def test_load_backlog():
    from tradeiobot.scrapers.howsitcoming import load_backlog
    items = load_backlog()
    assert len(items) == 9

def test_load_in_progress():
    from tradeiobot.scrapers.howsitcoming import load_in_progress
    items = load_in_progress()
    assert len(items) == 6

def test_load_pending_deployment():
    from tradeiobot.scrapers.howsitcoming import load_pending_deployment
    items = load_pending_deployment()
    assert len(items) == 4
