# bybit_sniper_engine.py

from bybit_feed import get_bybit_sniper_feed, fetch_orderbook
from sniper_score import score_vsplit_vwap
from trap_journal import log_sniper_event
from discord_alert import send_discord_alert
from datetime import datetime
import numpy as np

print("[✓] Bybit Sniper Engine Started for BTC-USDT...")

def run_bybit_sniper():
    df = get_bybit_sniper_feed()
    if df is None or len(df) < 20:
        return

    try:
        close_prices = df['close'].astype(float).tolist()
        rsi_series = df['rsi'].astype(float).tolist()
        last_close = float(close_prices[-1])
        vwap = float(df['vwap'].iloc[-1]) if 'vwap' in df.columns else np.mean(close_prices)

        orderbook = fetch_orderbook()
        bids = float(orderbook.get("bids", 1.0))
        asks = float(orderbook.get("asks", 1.0))

        score, reasons = score_vsplit_vwap({
            "rsi": rsi_series,
            "price": last_close,
            "vwap": vwap,
            "bids": bids,
            "asks": asks
        })

        if score >= 2:
            spoof_ratio = round(bids / asks, 3) if asks != 0 else 0.0
            trap = {
                "symbol": "BTC/USDT",
                "exchange": "Bybit",
                "timestamp": datetime.utcnow().isoformat(),
                "entry_price": last_close,
                "vwap": round(vwap, 2),
                "rsi": round(rsi_series[-1], 2),
                "score": score,
                "reasons": reasons,
                "trap_type": "RSI-V + VWAP Trap",
                "spoof_ratio": spoof_ratio,
                "bias": "Below" if last_close < vwap else "Above",
                "rsi_status": "V-Split" if "split" in str(reasons).lower() else "None",
                "vsplit_score": "VWAP Zone" if "vwap" in str(reasons).lower() else "None",
                "confidence": score,
                "flow_reason": "Below VWAP" if last_close < vwap else "Above VWAP"
            }
            log_sniper_event(trap)
            send_discord_alert(trap)
            print("[TRIGGER] Bybit Sniper Entry:", trap)
        else:
            print(f"[BYBIT SNIPER] No trap. Score: {score}, RSI: {rsi_series[-1]}, Price: {last_close}")

    except Exception as e:
        print(f"[!] Bybit Engine Error:", e)
