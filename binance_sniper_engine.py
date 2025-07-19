# binance_sniper_engine.py

from binance_feed import get_binance_sniper_feed, fetch_orderbook
from sniper_score import score_vsplit_vwap
from trap_journal import log_sniper_event
from discord_alert import send_discord_alert
from datetime import datetime
import numpy as np

print("[✓] Binance Sniper Engine Started for BTCUSDT...")

def run_binance_sniper():
    rows = get_binance_sniper_feed()
    if not rows or len(rows) < 20:
        print("[BINANCE SNIPER] Not enough data.")
        return

    try:
        close_prices = [row["close"] for row in rows]
        volumes = [row["volume"] for row in rows]
        rsi_series = calculate_rsi_series(close_prices)
        last_close = close_prices[-1]
        vwap = np.average(close_prices, weights=volumes)

        orderbook = fetch_orderbook()
        bids = orderbook.get("bids", 1.0)
        asks = orderbook.get("asks", 1.0)

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
                "exchange": "Binance",
                "timestamp": datetime.utcnow().isoformat(),
                "entry_price": last_close,
                "vwap": round(vwap, 2),
                "rsi": round(rsi_series[-1], 2),
                "score": score,
                "reasons": reasons
            }
            log_sniper_event(trap)
            send_discord_alert(trap)
            print("[TRIGGER] Binance Sniper Entry:", trap)
        else:
            print(f"[BINANCE SNIPER] No trap. Score: {score}, RSI: {rsi_series[-1]}, Price: {last_close}")

    except Exception as e:
        print(f"[!] Binance Engine Error: {e}")

def calculate_rsi_series(closes, period=14):
    if len(closes) < period + 1:
        return [50.0] * len(closes)
    deltas = np.diff(closes)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = [100. - 100. / (1. + rs)]
    for delta in deltas[period:]:
        gain = max(delta, 0)
        loss = -min(delta, 0)
        up = (up * (period - 1) + gain) / period
        down = (down * (period - 1) + loss) / period
        rs = up / down if down != 0 else 0
        rsi.append(100. - 100. / (1. + rs))
    return [50.0] * (len(closes) - len(rsi)) + rsi
