# kucoin_feed.py
import requests
import pandas as pd

KCS_BASE_URL = "https://api.kucoin.com"

def get_kucoin_sniper_feed(symbol="BTC-USDT", interval="1min", limit=100):
    url = f"{KCS_BASE_URL}/api/v1/market/candles"
    params = {"symbol": symbol, "type": interval}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json().get("data", [])[:limit]
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df = df.astype(float)
        df = df.sort_index(ascending=True).reset_index(drop=True)
        df["vwap"] = df["turnover"] / df["volume"]

        delta = df["close"].diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = -delta.clip(upper=0).rolling(window=14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))
        df["rsi"] = df["rsi"].fillna(50)

        return df.tail(20)
    except Exception as e:
        print(f"[!] Error fetching KuCoin feed: {e}")
        return None

def fetch_orderbook(symbol="BTC-USDT"):
    try:
        url = f"{KCS_BASE_URL}/api/v1/market/orderbook/level2_20"
        params = {"symbol": symbol}
        res = requests.get(url, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()["data"]
        bid_total = sum(float(b[1]) for b in data["bids"])
        ask_total = sum(float(a[1]) for a in data["asks"])
        return {"bids": bid_total, "asks": ask_total}
    except Exception as e:
        print(f"[!] Error fetching KuCoin orderbook: {e}")
        return {"bids": 1.0, "asks": 1.0}
