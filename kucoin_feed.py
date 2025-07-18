# kucoin_feed.py
import requests

KCS_BASE_URL = "https://api.kucoin.com"

def fetch_klines(symbol="BTC-USDT", interval="1min", limit=100):
    url = f"{KCS_BASE_URL}/api/v1/market/candles"
    params = {"symbol": symbol, "type": interval}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json().get("data", [])[:limit]
    except Exception as e:
        print(f"[!] Error fetching klines: {e}")
        return []

def fetch_orderbook(symbol="BTC-USDT"):
    url = f"{KCS_BASE_URL}/api/v1/market/orderbook/level2_20"
    params = {"symbol": symbol}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json().get("data", {})
        bids = data.get("bids", [])
        asks = data.get("asks", [])
        total_bids = sum(float(b[1]) for b in bids)
        total_asks = sum(float(a[1]) for a in asks)
        return {"bids": total_bids, "asks": total_asks}
    except Exception as e:
        print(f"[!] Error fetching orderbook: {e}")
        return {"bids": 1.0, "asks": 1.0}
