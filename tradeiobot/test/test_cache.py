import time
from unittest.mock import MagicMock
from tradeiobot.cache import cache

def test_cache():
    mock = MagicMock()
    cached_mock = cache("aKey", 99)(mock) # cache results for 99 seconds
    cached_mock(1)
    cached_mock(2)
    assert mock.call_count == 1

def test_cache_expiry():
    mock = MagicMock()
    cached_mock = cache("aKey", 0)(mock)
    cached_mock(1)
    time.sleep(1) # allow cache to expire
    cached_mock(2)
    assert mock.call_count == 2