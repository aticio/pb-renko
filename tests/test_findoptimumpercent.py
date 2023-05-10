from pbrenko import PbRenko
import requests
from decimal import Decimal, getcontext

BINANCE_URL = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"
INTERVAL = "1d",
LIMIT = 129
PARAMS = {"symbol": SYMBOL, "interval": INTERVAL, "limit": LIMIT}


def test_findoptimumpercent():
    response = requests.get(url=BINANCE_URL, params=PARAMS)
    data = response.json()
    close = [float(c[4]) for c in data]
    close.pop()

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
            print(k)
            break
