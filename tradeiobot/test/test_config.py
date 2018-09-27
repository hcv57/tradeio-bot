import os
import pytest

def test_missing_config():
    with pytest.raises(ValueError):
        import tradeiobot.config

def test_valid_config():
    os.environ["TELEGRAM_TOKEN"] = "t0ken"
    import tradeiobot.config