from pbrenko import PbRenko
import requests

BINANCE_URL = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"
INTERVAL = "1d",
LIMIT = 129
PARAMS = {"symbol": SYMBOL, "interval": INTERVAL, "limit": LIMIT}


def test_drawpbrenko():
    response = requests.get(url=BINANCE_URL, params=PARAMS)
    data = response.json()
    close = [float(c[4]) for c in data]
    close.pop()

    pbrnk = PbRenko(5.6, close)
    pbrnk.create_pbrenko()

    pbrnk.draw_chart()
