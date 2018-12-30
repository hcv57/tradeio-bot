from tradeiobot.util import dotdict


import tradeiobot.db
import tradeiobot.db.stores

# patch connection to use memory store only
tradeiobot.db.connection = tradeiobot.db.connect([tradeiobot.db.stores.memory])

import tradeiobot.stats


def create_dummy_telegram_update(user_id=0):
    return dotdict(dict(
        message=dotdict(dict(
            from_user=dotdict(dict(
                id=user_id
            ))
        ))
    ))

@tradeiobot.stats.track
def dummy_telegram_handler(_bot, _update):
    pass


def test_initial_stats():
    assert tradeiobot.stats.get_hits() == 0
    assert tradeiobot.stats.get_unique_users() == 0
    assert tradeiobot.stats.get_uptime() > 0

def test_track_hits():
    dummy_telegram_handler(None, create_dummy_telegram_update())
    assert tradeiobot.stats.get_hits() == 1
    dummy_telegram_handler(None, create_dummy_telegram_update())
    assert tradeiobot.stats.get_hits() == 2

def test_get_unique_users():
    dummy_telegram_handler(None, create_dummy_telegram_update())
    assert tradeiobot.stats.get_unique_users() == 1
    dummy_telegram_handler(None, create_dummy_telegram_update("user2"))
    assert tradeiobot.stats.get_unique_users() == 2
