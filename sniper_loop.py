# sniper_loop.py
import time
from btc_sniper_engine import run_btc_sniper
from bybit_sniper_engine import run_bybit_sniper
from binance_sniper_engine import run_binance_sniper
from dotenv import load_dotenv
import os

load_dotenv()

print("[LOOP] Starting sniper loop...")

while True:
    print("\n[LOOP] 🔁 TICK — New Sniper Cycle")

    try:
        print("[LOOP] Running KuCoin sniper...")
        run_btc_sniper()
    except Exception as e:
        print(f"[ERROR] KuCoin sniper failed: {e}")

    try:
        print("[LOOP] Running Bybit sniper...")
        run_bybit_sniper()
    except Exception as e:
        print(f"[ERROR] Bybit sniper failed: {e}")

    try:
        print("[LOOP] Running Binance sniper...")
        run_binance_sniper()
    except Exception as e:
        print(f"[ERROR] Binance sniper failed: {e}")

    print("[LOOP] 💤 Sleeping for 60 seconds\n")
    time.sleep(60)
