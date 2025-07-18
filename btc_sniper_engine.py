import os
import time
from datetime import datetime, timezone

from kucoin_feed import fetch_klines, fetch_orderbook
from sniper_score import score_vsplit_vwap
from discord_alert import send_discord_alert
from memory_store import remember_trap
from vwap_levels import get_vwap_levels
from cvd_divergence import detect_cvd_divergence

# 🧠 Sniper tools (excluding POC Wick)
from sniper_tools.delta_spike_engine import detect_delta_spike
from sniper_tools.heatmap_sweep_engine import detect_heatmap_sweep
from sniper_tools.vwap_rejection_engine import detect_vwap_rejection
from sniper_tools.sniper_confluence_score import calculate_confluence_score

symbol = "BTC-USDT"
print(f"[⚡] BTC Sniper Engine Started for {symbol}...")

while True:
    try:
        # === Fetch Candle Data ===
        klines = fetch_klines(symbol)
        if not klines or len(klines) < 30:
            print("[!] Not enough candle data.")
            time.sleep(10)
            continue

        latest = klines[-1]
        price = float(latest[2])
        wick_high = float(latest[3])
        wick_low = float(latest[4])
        volume = float(latest[5])
        delta = float(latest[6]) if len(latest) > 6 else 0.0

        volume_series = [float(k[5]) for k in klines[-30:]]
        price_series = [float(k[2]) for k in klines[-30:]]
        rsi_series = [float(k[2]) for k in klines[-15:]]
        cvd_series = [float(k[5]) for k in klines[-30:]]

        vwap = sum(float(k[2]) * float(k[5]) for k in klines[-20:]) / max(1, sum(float(k[5]) for k in klines[-20:]))

        ob = fetch_orderbook(symbol)
        bids = ob.get("bids", 1.0)
        asks = ob.get("asks", 1.0)
        spoof_ratio = round(bids / asks, 3) if asks else 1.0

        vwap_map = get_vwap_levels()
        daily = vwap_map.get("daily")
        weekly = vwap_map.get("weekly")
        monthly = vwap_map.get("monthly")

        # === Core Scoring ===
        score_data = score_vsplit_vwap({
            "rsi": rsi_series,
            "price": price,
            "vwap": vwap,
            "volume": volume_series,
            "cvd": cvd_series,
            "price_series": price_series,
            "bids": bids,
            "asks": asks
        })

        if not score_data:
            print("[~] No valid sniper signal.")
            time.sleep(10)
            continue

        confidence = score_data[0]
        reasons = score_data[1]
        bias = "Below" if price < vwap else "Above"
        score = min(confidence * 10, 99)

        # === Delta Spike Detection ===
        latest_candle = {
            "timestamp": latest[0],
            "delta": delta,
            "volume": volume
        }
        delta_result = detect_delta_spike(latest_candle)
        if delta_result.get("spike_detected"):
            reasons.append(f"Delta Spike: Δ={delta_result['delta_value']}, Vol={delta_result['volume']}")

        # === POC Wick Detection (DISABLED) ===
        # poc_level = vwap
        # print("[TEST] POC Wick check")
        # poc_result = detect_poc_wick(wick_high, wick_low, poc_level)
        # if poc_result:
        #     reasons.append(poc_result)

        # === Heatmap Sweep Detection ===
        heatmap_clusters = []  # Placeholder for future integration
        sweep_result = detect_heatmap_sweep(symbol, heatmap_clusters)
        if sweep_result:
            reasons.append(sweep_result)

        # === VWAP Rejection Detection ===
        previous_price = float(klines[-2][2])
        reject_result = detect_vwap_rejection(price_series, vwap, previous_price)
        if reject_result:
            reasons.append(reject_result)

        # === CVD Divergence ===
        cvd_result = detect_cvd_divergence(price_series, cvd_series)
        if cvd_result.get("divergence"):
            reasons.append(cvd_result["reason"])

        # === Final Scoring ===
        score = calculate_confluence_score(confidence, spoof_ratio, reasons)

        # === Alert Package ===
        trade_data = {
            "symbol": symbol,
            "price": price,
            "vwap": vwap,
            "trap_type": "RSI-V Split + VWAP",
            "rsi_status": "RSI V-Split Detected",
            "confidence": confidence,
            "spoof_ratio": spoof_ratio,
            "bias": bias,
            "score": score,
            "reasons": reasons,
            "vwap_daily": daily,
            "vwap_weekly": weekly,
            "vwap_monthly": monthly,
            "time": datetime.now(timezone.utc).isoformat()
        }

        remember_trap(symbol, trade_data)
        send_discord_alert(trade_data)
        print(f"[📡] Alert Sent: {trade_data}")

        time.sleep(15)

    except Exception as e:
        print(f"[!] Engine Error: {e}")
        time.sleep(10)
