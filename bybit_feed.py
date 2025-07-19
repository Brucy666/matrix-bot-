# bybit_feed.py
import requests

BYBIT_BASE_URL = "https://api.bybit.com"

def get_bybit_sniper_feed(symbol="BTCUSDT"):
    try:
        klines = requests.get(f"{BYBIT_BASE_URL}/v5/market/kline",
                              params={"category": "linear", "symbol": symbol, "interval": "1", "limit": 20})
        klines.raise_for_status()
        raw = klines.json()["result"]["list"]
        data = [
            {
                "timestamp": int(row[0]),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[5])
            }
            for row in raw
        ]
        return data
    except Exception as e:
        print(f"[!] Bybit Feed Error: {e}")
        return []

def fetch_orderbook(symbol="BTCUSDT"):
    try:
        orderbook = requests.get(f"{BYBIT_BASE_URL}/v5/market/orderbook",
                                 params={"category": "linear", "symbol": symbol})
        orderbook.raise_for_status()
        data = orderbook.json()["result"]
        bids = sum([float(entry[1]) for entry in data.get("b", [])])
        asks = sum([float(entry[1]) for entry in data.get("a", [])])
        return {"bids": bids, "asks": asks}
    except Exception as e:
        print(f"[!] Bybit Orderbook Error: {e}")
        return {"bids": 1.0, "asks": 1.0}
