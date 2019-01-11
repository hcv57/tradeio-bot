from tradeiobot.util import balance_changes

def test_balance_changes_none():
    current = dict(BTC=1.23, ETH=2.34)
    previous = dict(BTC=1.23, ETH=2.34)
    assert dict() == balance_changes(current, previous)

def test_balance_change_new_asset():
    current = dict(BTC=1.23, ETH=2.34)
    previous = dict(BTC=1.23)
    assert dict(ETH=2.34) == balance_changes(current, previous)

def test_balance_change_increased_asset():
    current = dict(BTC=1.23, ETH=2.35)
    previous = dict(BTC=1.23, ETH=2.34)
    assert dict(ETH=0.01) == balance_changes(current, previous)

def test_balance_change_decreased_asset():
    current = dict(BTC=1.23, ETH=2.33)
    previous = dict(BTC=1.23, ETH=2.34)
    assert dict(ETH=-0.01) == balance_changes(current, previous)

def test_balance_change_small_values():
    current = dict(BTC=1.23)
    previous = dict(BTC=1.22000001)
    assert dict(BTC=0.00999999) == balance_changes(current, previous)

