# btc_sniper_engine.py
# Sniper strategy logic for BTC/USDT using KuCoin data

from kucoin_feed import get_kucoin_sniper_feed
from sniper_score import score_vsplit_vwap
from trap_journal import log_sniper_event
from discord_alert import send_discord_alert
from datetime import datetime
import numpy as np

print("[✓] BTC Sniper Engine Started for BTC-USDT...")

def run_btc_sniper():
    df = get_kucoin_sniper_feed()
    if df is None or len(df) < 20:
        return

    try:
        # Extract close prices as flat float list
        close_prices = df['close'].astype(float).tolist()
        volume = df['volume'].astype(float).tolist()

        # Use most recent values
        last_close = float(close_prices[-1])
        vwap = float(df['vwap'].iloc[-1]) if 'vwap' in df.columns else np.mean(close_prices)
        rsi = float(df['rsi'].iloc[-1]) if 'rsi' in df.columns else 50.0

        # Core sniper trap logic
        if rsi < 45 and last_close < vwap:
            score = score_sniper_signal(rsi=rsi, vwap=vwap, price=last_close)
            trap = {
                "symbol": "BTC/USDT",
                "exchange": "KuCoin",
                "timestamp": datetime.utcnow().isoformat(),
                "entry_price": last_close,
                "vwap": round(vwap, 2),
                "rsi": round(rsi, 2),
                "reason": "RSI-V + VWAP Trap",
                "score": score
            }
            log_sniper_event(trap)
            send_discord_alert(trap)
            print("[TRIGGER] Sniper Entry:", trap)
        else:
            print("[BTC SNIPER] No valid sniper setup.")

    except Exception as e:
        print(f"[!] Engine Error: {e}")
