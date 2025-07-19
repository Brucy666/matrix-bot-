# bybit_sniper_engine.py
# Bybit sniper trap detection engine

from bybit_feed import get_bybit_sniper_feed, fetch_orderbook
from sniper_score import score_vsplit_vwap
from discord_alert import send_discord_alert
from trap_journal import log_sniper_event
from datetime import datetime
import numpy as np

print("[+] Bybit Sniper Engine Started for BTC-USDT...")

def run_bybit_sniper():
    df = get_bybit_sniper_feed()
    if df is None or len(df) < 20:
        return

    try:
        # Extract historical market data
        close_prices = df['close'].astype(float).tolist()
        rsi_series = df['rsi'].astype(float).tolist()
        volume = df['volume'].astype(float).tolist()

        # Most recent values
        last_close = float(close_prices[-1])
        vwap = float(df['vwap'].iloc[-1]) if 'vwap' in df.columns else np.mean(close_prices)

        # Spoof ratio from Bybit L2 snapshot
        orderbook = fetch_orderbook()
        bids = float(orderbook.get("bids", 1.0))
        asks = float(orderbook.get("asks", 1.0))

        # Scoring engine
        score, reasons = score_vsplit_vwap({
            "rsi": rsi_series,
            "price": last_close,
            "vwap": vwap,
            "bids": bids,
            "asks": asks
        })

        if score >= 2:
            trap = {
                "symbol": "BTC/USDT",
                "exchange": "Bybit",
                "timestamp": datetime.utcnow().isoformat(),
                "entry_price": last_close,
                "vwap": round(vwap, 2),
                "rsi": round(rsi_series[-1], 2),
                "score": score,
                "reasons": reasons
            }
            log_sniper_event(trap)
            send_discord_alert(trap)
            print("[TRIGGER] Bybit Sniper Entry:", trap)
        else:
            print(f"[BYBIT SNIPER] No trap. Score: {score}, RSI: {rsi_series[-1]}, Price: {last_close}")

    except Exception as e:
        print(f"[!] Bybit Sniper Engine Error: {e}")
