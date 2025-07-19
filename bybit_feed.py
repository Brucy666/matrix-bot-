# ✅ bybit_feed.py (rewrite)
import requests
import pandas as pd
import numpy as np

def get_bybit_sniper_feed():
    try:
        url = "https://api.bybit.com/v5/market/kline"
        params = {
            "category": "linear",
            "symbol": "BTCUSDT",
            "interval": "1",
            "limit": 20
        }
        res = requests.get(url, params=params)
        data = res.json().get("result", {}).get("list", [])

        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "turnover"])
        df = df.astype({"close": float, "volume": float})
        df["vwap"] = df["turnover"].astype(float) / df["volume"]

        # Dummy RSI logic for now (placeholder)
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        df["rsi"] = rsi.fillna(50)

        return df.tail(20)

    except Exception as e:
        print(f"[!] Bybit Feed Error: {e}")
        return None


def fetch_orderbook():
    try:
        url = "https://api.bybit.com/v5/market/orderbook"
        params = {"category": "linear", "symbol": "BTCUSDT"}
        res = requests.get(url, params=params)
        ob = res.json().get("result", {}).get("b", [])
        bids = sum(float(b[1]) for b in res.json().get("result", {}).get("b", []))
        asks = sum(float(a[1]) for a in res.json().get("result", {}).get("a", []))
        return {"bids": bids, "asks": asks}
    except:
        return {"bids": 1.0, "asks": 1.0}
