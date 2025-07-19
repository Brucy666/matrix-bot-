# bybit_feed.py
# Fixed: list index error for sniper engine

import requests

BYBIT_BASE_URL = "https://api.bybit.com"

def get_bybit_sniper_feed(symbol="BTCUSDT"):
    try:
        url = f"{BYBIT_BASE_URL}/v5/market/kline"
        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": "1",
            "limit": 100
        }
        res = requests.get(url, params=params)
        data = res.json().get("result", {}).get("list", [])
        if not data:
            return None

        closes = [float(c[4]) for c in data]  # close prices
        vwap = sum(float(c[1]) * float(c[5]) for c in data) / sum(float(c[5]) for c in data)
        volume = sum(float(c[5]) for c in data)
        last_price = float(data[-1][4])

        return {
            "price": last_price,
            "closes": closes,
            "vwap": vwap,
            "volume": volume
        }

    except Exception as e:
        print(f"[BYBIT FEED ERROR] {e}")
        return None

def fetch_orderbook(symbol="BTCUSDT"):
    try:
        url = f"{BYBIT_BASE_URL}/v5/market/orderbook"
        params = {"category": "linear", "symbol": symbol}
        res = requests.get(url, params=params)
        orderbook = res.json().get("result", {})
        bids = sum(float(b[1]) for b in orderbook.get("b", []))
        asks = sum(float(a[1]) for a in orderbook.get("a", []))
        return {"bids": bids, "asks": asks}
    except:
        return {"bids": 1.0, "asks": 1.0}
