from pbrenko import PbRenko
import requests
from decimal import Decimal, getcontext
from numpy import log as ln

BINANCE_URL = "https://api.binance.com/api/v3/klines"
EXCHANGE_INFO = "https://api.binance.com/api/v3/exchangeInfo"
SYMBOL = "BTCUSDT"
INTERVAL = "1d",
LIMIT = 129


def test_bulkoptimum():
    exchange_info = get_exchange_info()
    pairs = get_pairs(exchange_info)
    usdt_pairs = filter_usdt_pairs(pairs)
    for p in usdt_pairs:
        close = get_data(p)
        percent = find_optimumpercent(close)
        if percent is None:
            continue
        pbrnk = PbRenko(percent, close)
        pbrnk.create_pbrenko()
        score = backtest(pbrnk.bricks, len(close))
        if score > 2:
            print(p, percent, score)


def find_optimumpercent(close):
    found_percentages = []
    for i in (x / 10 for x in range(9, 101)):
        pbrnk = PbRenko(i, close)
        pbrnk.create_pbrenko()
        if pbrnk.number_of_leaks == 0:
            found_percentages.append(i)

    getcontext().prec = 1
    for i, k in enumerate(found_percentages):
        all_equal = True
        for t, z in enumerate(found_percentages[i:]):
            if i + t != len(found_percentages) - 1:
                if (float(Decimal(found_percentages[i + t + 1]) - Decimal(found_percentages[i + t]))) != float(0.1):
                    all_equal = False
                    break
        if all_equal:
            return k
    return None


def backtest(bricks, tick_count):
    global RESULTS

    balance = 0
    sign_changes = 0
    for i, b in enumerate(bricks):
        if i != 0:
            if bricks[i]["type"] == bricks[i - 1]["type"]:
                balance = balance + 1
            else:
                balance = balance - 2
                sign_changes = sign_changes + 1

    price_ratio = tick_count / len(bricks)

    if sign_changes == 0:
        return -1.0
    score = balance / sign_changes
    if score >= 0 and price_ratio >= 1:
        score = ln(score + 1) * ln(price_ratio)
        return score
    else:
        score = -1.0
        return score
    # return
    # RESULTS.append({"brick_size": brick_size, "score": score})
    # print({"brick_size": brick_size, "score": score})


def get_data(symbol):
    params = {"symbol": symbol, "interval": INTERVAL, "limit": LIMIT}
    response = requests.get(url=BINANCE_URL, params=params)
    data = response.json()
    close = [float(c[4]) for c in data]
    close.pop()
    return close


def filter_usdt_pairs(pairs):
    usdt_pairs = []
    for pair in pairs:
        if "USDT" in pair and "USDC" not in pair and "USDC" not in pair:
            usdt_pairs.append(pair)
    return usdt_pairs


def get_pairs(exchange_info):
    pairs = []
    for symbol in exchange_info["symbols"]:
        pairs.append(symbol["symbol"])
    return pairs


def get_exchange_info():
    response = requests.get(EXCHANGE_INFO)
    exchange_info = response.json()
    return exchange_info
