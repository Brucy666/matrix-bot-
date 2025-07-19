# binance_sniper_engine.py
from binance_feed import get_binance_sniper_feed, fetch_orderbook
from sniper_score import score_vsplit_vwap
from discord_alert import send_discord_alert
from trap_journal import log_sniper_event
from gpt_money_flow import calculate_gpt_money_flow
from datetime import datetime
import numpy as np

print("[+] Binance Sniper Engine Started for BTCUSDT...")

def run_binance_sniper():
    df = get_binance_sniper_feed()
    if df is None or len(df) < 20:
        return

    try:
        close_prices = df['close'].astype(float).tolist()
        rsi_series = df['rsi'].astype(float).tolist()
        volume = df['volume'].astype(float).tolist()

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

        flow = None
        try:
            flow = calculate_gpt_money_flow(
                price=last_close,
                vwap=vwap,
                volume=volume[-1],
                rsi_slope=rsi_series[-1] - rsi_series[-2],
                spoof_ratio=bids / max(asks, 0.001)
            )
        except Exception as e:
            print(f"[!] Binance Money Flow Error: {e}")

        if score >= 2:
            trap = {
                "symbol": "BTC/USDT",
                "exchange": "Binance",
                "timestamp": datetime.utcnow().isoformat(),
                "entry_price": last_close,
                "vwap": round(vwap, 2),
                "rsi": round(rsi_series[-1], 2),
                "score": score,
                "reasons": reasons,
            }
            if flow:
                trap.update({
                    "money_flow_score": flow.get("money_flow_score"),
                    "bias": flow.get("bias"),
                    "flow_reason": flow.get("reason")
                })

            log_sniper_event(trap)
            send_discord_alert(trap)
            print("[TRIGGER] Binance Sniper Entry:", trap)
        else:
            print(f"[BINANCE SNIPER] No trap. Score: {score}, RSI: {rsi_series[-1]}, Price: {last_close}")

    except Exception as e:
        print(f"[!] Binance Engine Error: {e}")
