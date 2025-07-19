# bybit_feed.py
import requests

BYBIT_BASE_URL = "https://api.bybit.com"

def get_bybit_sniper_feed(symbol="BTCUSDT", interval="1"):
    url = f"{BYBIT_BASE_URL}/v5/market/kline"
    params = {"symbol": symbol, "interval": interval, "limit": 100}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json().get("result", {}).get("list", [])
        if not data:
            return None
        # Format into rows with expected values
        rows = []
        for row in data:
            close = float(row[4])
            volume = float(row[5])
            rows.append({"close": close, "volume": volume})
        return rows
    except Exception as e:
        print(f"[!] Error fetching Bybit kline data: {e}")
        return None

def fetch_orderbook(symbol="BTCUSDT"):
    url = f"{BYBIT_BASE_URL}/v5/market/orderbook"
    params = {"category": "linear", "symbol": symbol}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json().get("result", {})
        bids = data.get("b", [])
        asks = data.get("a", [])
        bid_total = sum(float(b[1]) for b in bids)
        ask_total = sum(float(a[1]) for a in asks)
        return {"bids": bid_total, "asks": ask_total}
    except Exception as e:
        print(f"[!] Error fetching Bybit orderbook: {e}")
        return {"bids": 1.0, "asks": 1.0}
