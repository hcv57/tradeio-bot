from unittest.mock import MagicMock

from tradeiobot.db.stores import memory


def test_do_get():
    assert None == memory.do_get("Table", "Key")


def test_do_set():
    assert None == memory.do_set("T", "K", "V")
    assert "V" == memory.do_get("T", "K")
    assert None == memory.do_set("T", "K", "V2")
    assert "V2" == memory.do_get("T", "K")


def test_do_get_all_as_dict():
    assert dict() == memory.do_get_all_as_dict("T2")
    memory.do_set("T2", "K", "V")
    memory.do_set("T2", "K2", "V2")
    assert {'K': 'V', 'K2': 'V2'} == memory.do_get_all_as_dict("T2")


def test_do_delete():
    assert None == memory.do_delete("T3", "K")
    memory.do_set("T3", "K", "V")
    memory.do_delete("T3", "K")
    assert None == memory.do_get("T3", "K")


## Methods inheritted from Abstractstore for the high level api

def test_get():
    next_store_action = MagicMock(return_value=None)  # usually partially applied in tradeiobot.db.connection
    assert None == memory.get("table-miss", "key", next_store_action)
    next_store_action.assert_called_once_with("table-miss", "key")  # to check the next store


def test_set():
    next_store_action = MagicMock(return_value=None)
    assert None == memory.set("table", "key", "value", next_store_action)
    next_store_action.assert_called_once_with("table", "key", "value")  # to propagate to the next store

    next_store_action = MagicMock(return_value=None)
    assert "value" == memory.get("table", "key", next_store_action)
    next_store_action.assert_not_called()


def test_get_all_as_dict():
    next_store_action = MagicMock()
    memory.set("x", "y", "z", next_store_action)
    memory.set("x", "y2", "z2", next_store_action)
    memory.set("x", "y2", "z3", next_store_action)  # overwriting the previous memory.set
    assert {'y': 'z', 'y2': 'z3'} == memory.get_all_as_dict("x", next_store_action)


def test_delete():
    next_store_action = MagicMock()
    assert None == memory.delete("lorem", "ipsum", next_store_action)

    memory.set("lorem", "ipsum", "dolor", next_store_action)
    memory.delete("lorem", "ipsum", next_store_action)

    next_store_action = MagicMock(return_value=None)
    assert None == memory.get("lorem", "ipsum", next_store_action)

def test_upward_propagation():
    # For downward propagation see the asserted calls to next_store_action Mock above

    next_store_action = MagicMock(return_value="Hello")

    assert "Hello" == memory.get("dummy", "key", next_store_action)
    next_store_action.assert_called_once_with("dummy", "key")

    next_store_action = MagicMock(return_value="Not called")
    assert "Hello" == memory.get("dummy", "key", next_store_action)

