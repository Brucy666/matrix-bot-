# binance_sniper_engine.py

from binance_feed import get_binance_sniper_feed, fetch_orderbook
from sniper_score import score_vsplit_vwap
from trap_journal import log_sniper_event
from discord_alert import send_discord_alert
from datetime import datetime
import numpy as np

print("[✓] Binance Sniper Engine Started for BTC-USDT...")

def run_binance_sniper():
    df = get_binance_sniper_feed()
    if df is None or len(df) < 20:
        return

    try:
        # Prepare market data
        close_prices = df['close'].astype(float).tolist()
        rsi_series = df['rsi'].astype(float).tolist()
        volume = df['volume'].astype(float).tolist()
        vwap = float(df['vwap'].iloc[-1]) if 'vwap' in df.columns else np.mean(close_prices)
        last_close = float(close_prices[-1])

        # Get spoof ratio from orderbook
        orderbook = fetch_orderbook()
        bids = float(orderbook.get("bids", 1.0))
        asks = float(orderbook.get("asks", 1.0))

        # Scoring logic
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
            print(f"[BINANCE SNIPER] No trap. Score: {score}, RSI: {rsi_series[-1]:.2f}, Price: {last_close}")

    except Exception as e:
        print(f"[!] Binance Sniper Engine Error: {e}")
