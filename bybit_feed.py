# bybit_feed.py
import requests
import pandas as pd

BYBIT_BASE_URL = "https://api.bybit.com"

def get_bybit_sniper_feed(symbol="BTCUSDT"):
    try:
        url = f"{BYBIT_BASE_URL}/v5/market/kline"
        params = {"category": "linear", "symbol": symbol, "interval": "1", "limit": 100}
        res = requests.get(url, params=params, timeout=5)
        raw = res.json().get("result", {}).get("list", [])
        if not raw:
            return None

        df = pd.DataFrame(raw, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "turnover"
        ])
        df = df.astype(float)
        df["vwap"] = df["turnover"] / df["volume"]

        delta = df["close"].diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = -delta.clip(upper=0).rolling(window=14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))
        df["rsi"] = df["rsi"].fillna(50)

        return df.tail(20)
    except Exception as e:
        print(f"[!] Bybit Feed Error: {e}")
        return None

def fetch_orderbook(symbol="BTCUSDT"):
    try:
        url = f"{BYBIT_BASE_URL}/v5/market/orderbook"
        params = {"category": "linear", "symbol": symbol}
        res = requests.get(url, params=params, timeout=5)
        res.raise_for_status()
        ob = res.json().get("result", {})
        bids = sum(float(b[1]) for b in ob.get("b", []))
        asks = sum(float(a[1]) for a in ob.get("a", []))
        return {"bids": bids, "asks": asks}
    except Exception as e:
        print(f"[!] Bybit Orderbook Error: {e}")
        return {"bids": 1.0, "asks": 1.0}
