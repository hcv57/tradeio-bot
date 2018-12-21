import requests
from bs4 import BeautifulSoup

import tradeiobot.config
from tradeiobot.cache import cache

@cache("CMC_EXCHANGEVOLUMES", tradeiobot.config.CMC_EXCHANGEVOLUMES_CACHE_FOR_SECONDS)
def _load_exchangevolumes_soup():
    html = requests.get(tradeiobot.config.CMC_EXCHANGEVOLUMES_URL).content
    return BeautifulSoup(html, "html.parser")

def load_cmc_data():
    s = _load_exchangevolumes_soup()
    tag = s.find(id='trade-io')
    return dict(
        rank=tag.td.h3.text.split(".")[0],
        volume=float(tag.find_next(id=True).find_previous(class_="volume")["data-usd"])
    )