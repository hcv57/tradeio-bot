import tradeiobot.apis.cmc

def load_token_ticker():
    ticker = tradeiobot.apis.cmc.load_token_ticker()
    data = ticker["data"]
    usd_quotes = data["quotes"]["USD"]
    return dict(
        name=data["name"],
        rank=data["rank"],
        circulating_supply=data["circulating_supply"],
        total_supply=data["total_supply"],
        price_usd=usd_quotes["price"],
        volume_24h_usd=usd_quotes["volume_24h"],
        market_cap_usd=usd_quotes["market_cap"]
    )

