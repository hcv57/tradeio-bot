import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


from tradeiobot.db import connect

c = connect()
c.set("table1", "sausage", "roll")
c.set("table1", "sausage", "roll2")
c.set("table1", "sausag222e", "roll2")
c.get("table1", "sausage")
r = c.get_all_as_dict("table1")
from tradeiobot.bot import start

# start()
