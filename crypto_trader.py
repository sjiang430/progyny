import logging

from collections import defaultdict
from datetime import datetime, timedelta
from statistics import mean

from crypto_api import get_coins, get_coin_price_history, submit_order
from db import save_quote, save_trade, get_trade_history


def trade():
    logging.info('--- parsing quotes ---')
    # get all quotes
    quotes = get_coins()
    save_quote(quotes)

    # get top 3 by market cap
    top_quotes = sorted(quotes, key=lambda x: x['market_cap'], reverse=True)[:3]
    for quote in top_quotes:
        # get avg price
        avg = _fetch_coin_avg_prices(quote['id'])
        if quote['current_price'] < avg:
            # order it
            order(quote, 1, avg)

            # save trade history
            save_trade(quote, 1)
        else:
            logging.info('%s cur_price %s > avg_price %s', quote['id'], quote['current_price'], avg)

    # calculate portfolio
    logging.info('--- calculating portfolio ---')
    _calc_portfolio(quotes)


def _calc_portfolio(quotes):
    coin2portfolio = defaultdict(float)
    for quote in quotes:
        coin_id = quote['id']
        current_price = quote['current_price']
        if quote['id'] in coin2portfolio:
            continue

        net = 0
        total_amount = 0
        trade_history = get_trade_history(coin_id)
        for th in trade_history:
            amount = th[3]
            price = th[2]
            total_amount += amount

            net += amount * (current_price - price)

        coin2portfolio[coin_id] = round(net, 2)
        logging.info('coin %s, owned %s, gain %s', coin_id, total_amount, coin2portfolio[coin_id])


def _fetch_coin_avg_prices(coin_id: str) -> float:
    time_prices = get_coin_price_history(coin_id)
    if not time_prices:
        logging.fatal('failed to get %s price history', coin_id)
        return -1

    starter_time = _n_days_ago(10)
    prices = []
    for time, price in time_prices:
        if time >= starter_time:
            prices.append(price)

    return mean(prices)


def order(coin, count, avg_prices):
    logging.info('%s cur_price %s < avg_price %s', coin['id'], coin['current_price'], avg_prices)
    
    logging.info('Ordering %s', coin['id'])
    submit_order(coin['id'], count, coin['current_price'])


def _n_days_ago(n: int) -> float:
    now = datetime.now()
    before = now - timedelta(days=n)
    return datetime(before.year, before.month, before.day).timestamp() * 1000


