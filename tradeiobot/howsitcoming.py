import requests
from bs4 import BeautifulSoup

import tradeiobot.config
from tradeiobot.cache import cache

@cache("HOWSITCOMING", tradeiobot.config.HOWSITCOMING_CACHE_FOR_SECONDS)
def _load_howsitcoming_soup():
    html = requests.get(tradeiobot.config.HOWSITCOMING_URL).content
    return BeautifulSoup(html, "html.parser")


def _load_section_items(section):
    return list(map(
        lambda item: item.p.text,
        _load_howsitcoming_soup().find(
            "section", class_="current-task-list"
        ).find_all(
            "div", class_="col-md-4"
        )[section].find_all(
            "div", class_="task-card"
        )
    ))

load_backlog = lambda: _load_section_items(0)
load_in_progress = lambda: _load_section_items(1)
load_pending_deployment = lambda: _load_section_items(2)
