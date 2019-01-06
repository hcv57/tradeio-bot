import datetime
import itertools
import json

from tradeioapi.api.trading import account_get

import tradeiobot.config
import tradeiobot.markets
import tradeiobot.releasenotes
from tradeiobot.scrapers import cmc, howsitcoming
import tradeiobot.stats
import tradeiobot.token
from tradeiobot import config
from tradeiobot.bot.keyboards import main_keyboard

from tradeiobot.db import connection


@tradeiobot.stats.track
def start_handler(bot, update):
    update.message.reply_html("\n".join([
        "<b>Welcome to the Trade.io Bot (unofficial)</b>\n",
        "The following commands are currently available:\n",
        "/markets - List of all instruments",
        "/volume - 24h exchange volume",
        "/exchange - Trade.io on CMC",
        "/token - TIOx on CMC",
        "/progress - Trade.io progress tracker",
        "/about - Usage stats and additional info"
    ]), reply_markup=main_keyboard())


@tradeiobot.releasenotes.showonce
@tradeiobot.stats.track
def progress_handler(bot, update):
    update.message.reply_markdown("\n".join(
        itertools.chain(
            ["*Trade.io Progress Tracker*"],
            [""],
            ["*Backlog*"],
            map(lambda i: "▪ {}".format(i), howsitcoming.load_backlog()),
            [""],
            ["*In progress*"],
            map(lambda i: "▪ {}".format(i), howsitcoming.load_in_progress()),
            [""],
            ["*Pending deployment*"],
            map(lambda i: "▪ {}".format(i), howsitcoming.load_pending_deployment()),
            [""],
            ["_Source: http://howsitcoming.trade.io_"]
        )
    ), reply_markup=main_keyboard())


@tradeiobot.releasenotes.showonce
@tradeiobot.stats.track
def markets_handler(bot, update):
    instruments = tradeiobot.markets.get_instruments()
    response_buffer = ["<b>Trade.io Exchange Instruments</b>"]
    last_market_from = None
    for market in sorted(instruments.keys()):
        from_, to = market.split("_")
        if not last_market_from or not market.startswith(last_market_from):
            response_buffer.append("\n<b>{} markets</b>".format(from_))
        last_market_from = from_
        precision = get_precision_for_currency(to)
        response_buffer.append(
            (
                    "{trend_symbol} /{market} "
                    "{close:." + precision + "f} {to}"
            ).format(
                trend_symbol=get_trend_symbol(instruments[market]),
                market=market,
                close=instruments[market]["close"],
                to=to
            )
        )
    update.message.reply_html("\n".join(response_buffer), reply_markup=main_keyboard())


def get_precision_for_currency(to):
    return "4" if to == "USDT" else "8"


def get_trend_symbol(instrument):
    opening = instrument["open"]
    closing = instrument["close"]
    if closing > opening:
        return "↗"
    elif closing < opening:
        return "↘"
    else:
        return "➡"


@tradeiobot.releasenotes.showonce
@tradeiobot.stats.track
def volume_handler(bot, update):
    volume = tradeiobot.markets.get_total_volume()
    update.message.reply_markdown("\n".join([
        "*24h Exchange Volume*\n",
        "{volume:,.2f} USDT",
        "",
        "Note: For the USDT conversion of all instruments the calculation is based on the Exchange's USDT markets for BTC, ETH, TIOx and TUSD.",
        config.SPONSOR_MESSAGE
    ]).format(volume=volume), reply_markup=main_keyboard())


# @tradeiobot.releasenotes.showonce
# @tradeiobot.stats.track
# def exchange_handler(bot, update):
#     update.message.reply_markdown("\n".join([
#         "*Trade.io on CMC*",
#         "",
#         "*Rank:* {rank}",
#         "*Volume:* {volume:,.2f} USD",
#         "",
#         "_Source: https://coinmarketcap.com/exchanges/volume/24-hour_"
#     ]).format(**cmc.load_cmc_data()), reply_markup=main_keyboard())

@tradeiobot.releasenotes.showonce
@tradeiobot.stats.track
def exchange_handler(bot, update):
    update.message.reply_markdown("\n".join([
        "*Trade.io on CMC*",
        "",
        "*Rank:* ?",
        "*Volume:* ? USD",
        "",
        "This functionality has been disabled. It may be reenabled in the future "
        "but will require bot users to provide their own CMC API keys.",
        "",
        "_Source: https://coinmarketcap.com/exchanges/volume/24-hour_"
    ]), reply_markup=main_keyboard())


@tradeiobot.releasenotes.showonce
@tradeiobot.stats.track
def instrument_handler(bot, update, groups):
    instrument_name = groups[0]  # groups comes from the regex used by the handler
    from_, to = instrument_name.split("_")
    instrument = tradeiobot.markets.get_instrument(instrument_name, enrich=True)
    precision = get_precision_for_currency(to)
    show_usdt = lambda k: "" if to == "USDT" else " ({%s:,.2f} USDT)" % k
    update.message.reply_markdown("\n".join([
        "*{instrument_name} Market* {trend_symbol}\n",
        "*Open:* {open:." + precision + "f} {to}" + show_usdt("open_usdt"),
        "*Close:* {close:." + precision + "f} {to}" + show_usdt("close_usdt"),
        "*High:* {high:." + precision + "f} {to}" + show_usdt("high_usdt"),
        "*Low:* {low:." + precision + "f} {to}" + show_usdt("low_usdt"),
        "*Volume:* {volume:f} {from_} ({volume_usdt:.2f} USDT)",
    ]).format(
        **instrument,
        instrument_name=instrument_name,
        trend_symbol=get_trend_symbol(instrument),
        from_=from_,
        to=to
    ), reply_markup=main_keyboard())


@tradeiobot.releasenotes.showonce
@tradeiobot.stats.track
def about_handler(bot, update):
    update.message.reply_markdown("\n".join([
        "*Trade.io Bot (unoffical)*",
        "",
        "*Uptime:* {uptime:0>8}",
        "*Requests served:* {hits}",
        "*Unique users:* {users}",
        "",
        "*Version:* {version}",
        "*Commit:* {commit}",
        "*License:* MIT",
        "",
        "_Contributions welcome!_",
        "https://github.com/hcv57/tradeio-bot"
    ]).format(
        uptime=str(datetime.timedelta(seconds=tradeiobot.stats.get_uptime())),
        hits=tradeiobot.stats.get_hits(),
        users=tradeiobot.stats.get_unique_users(),
        version=tradeiobot.config.VERSION,
        commit=tradeiobot.config.COMMIT
    ), reply_markup=main_keyboard(), disable_web_page_preview=True)


@tradeiobot.releasenotes.showonce
@tradeiobot.stats.track
def token_handler(bot, update):
    update.message.reply_markdown("\n".join([
        "*TIOx on CMC*",
        "",
        "*Price:* {price_usd:,.4f} USD",
        "*24h volume:* {volume_24h_usd:,.2f} USD",
        "*Marketcap:* {market_cap_usd:,.2f} USD",
        "",
        "*Circulating supply:* {circulating_supply:,.0f} TIO",
        "*Total supply:* {total_supply:,.0f} TIO",
        "",
        "*Rank:* {rank}",
        "",
        "_Source: https://coinmarketcap.com/currencies/trade-token-x_"
    ]).format(
        **tradeiobot.token.load_token_ticker()
    ), reply_markup=main_keyboard())


def releasenotes_handler(bot, update):
    with open("RELEASES") as f:
        update.message.reply_markdown(
            "*What's new?*\n\n" +
            f.read()
        )

@tradeiobot.releasenotes.showonce
@tradeiobot.stats.track
def balance_handler(bot, update):
    key = connection.get(update.message.from_user.id, "api_key")
    secret = connection.get(update.message.from_user.id, "api_secret")
    if not key:
        update.message.reply_markdown("\n".join([
            "*API Access not configured*",
            "",
            "To activate API access please use",
            "/api yourkey yoursecret"
        ]), reply_markup=main_keyboard())
    else:
        account_response = account_get(key, secret)
        if account_response.status_code != 200:
            update.message.reply_markdown("\n".join([
                "*Your Balance*",
                "",
                "Something went wrong.",
                "Please ensure your api credentials are correct.",
                "",
                "/api yourkey yoursecret",
            ]), reply_markup=main_keyboard())
        else:
            data = json.loads(account_response.text)
            balances = []
            for balance in sorted(data["balances"], key=lambda k: k['asset']):
                if float(balance["available"]) > 0:
                    balances.append(
                        "*{: <6}* {:}".format(
                            balance["asset"].upper(),
                            balance["available"])
                    )
            update.message.reply_markdown("\n".join([
                "*Your Balances*",
                ""
            ] + balances), reply_markup=main_keyboard())

def api_handler(bot, update, groups):
    key, secret = groups
    connection.set(update.message.from_user.id, "api_key", key)
    connection.set(update.message.from_user.id, "api_secret", secret)
    update.message.reply_markdown("\n".join([
        "*API settings saved*"
    ]), reply_markup=main_keyboard())
