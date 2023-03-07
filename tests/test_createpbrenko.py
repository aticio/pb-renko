from pbrenko import PbRenko
import requests

BINANCE_URL = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"
INTERVAL = "1d"
PARAMS = {"symbol": SYMBOL, "interval": INTERVAL}


def test_createpbrenko():
    response = requests.get(url=BINANCE_URL, params=PARAMS)
    data = response.json()
    close = [float(c[4]) for c in data]

    pbrnk = PbRenko(1, close)
    pbrnk.create_pbrenko()
