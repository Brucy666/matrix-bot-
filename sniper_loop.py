import time
from btc_sniper_engine import run_btc_engine
from bybit_sniper_engine import run_bybit_engine
from binance_sniper_engine import run_binance_engine

print("[LOOP] 🔁 Starting sniper loop...")

while True:
    print("\n[LOOP] 🌀 TICK — New Sniper Cycle")

    print("[LOOP] Running KuCoin sniper...")
    run_btc_engine()

    print("[LOOP] Running Bybit sniper...")
    run_bybit_engine()

    print("[LOOP] Running Binance sniper...")
    run_binance_engine()

    print("[LOOP] 💤 Sleeping for 60 seconds\n")
    time.sleep(60)
