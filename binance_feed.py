# binance_feed.py
import requests

BINANCE_BASE_URL = "https://api.binance.com"

def get_binance_sniper_feed(symbol="BTCUSDT", interval="1m", limit=100):
    url = f"{BINANCE_BASE_URL}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        rows = []
        for row in data:
            close = float(row[4])      # Closing price
            volume = float(row[5])     # Volume
            rows.append({"close": close, "volume": volume})
        return rows
    except Exception as e:
        print(f"[!] Error fetching Binance klines: {e}")
        return None

def fetch_orderbook(symbol="BTCUSDT"):
    url = f"{BINANCE_BASE_URL}/api/v3/depth"
    params = {"symbol": symbol, "limit": 100}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        bids = data.get("bids", [])
        asks = data.get("asks", [])
        bid_total = sum(float(b[1]) for b in bids)
        ask_total = sum(float(a[1]) for a in asks)
        return {"bids": bid_total, "asks": ask_total}
    except Exception as e:
        print(f"[!] Error fetching Binance orderbook: {e}")
        return {"bids": 1.0, "asks": 1.0}
