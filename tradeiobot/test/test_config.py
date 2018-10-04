import os
import pytest
import importlib

def test_missing_config():
    with pytest.raises(ValueError):
        import_config()

def test_valid_config():
    os.environ["TELEGRAM_TOKEN"] = "t0ken"
    import_config()

def import_config():
    import tradeiobot.config
    importlib.reload(tradeiobot.config)
