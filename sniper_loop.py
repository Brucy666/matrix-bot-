# sniper_loop.py
import time
from kucoin_feed import fetch_kucoin_data
from cvd_engine import compute_cvd
from memory_store import log_signal, get_recent_traps
from discord_alert import send_alert

from dotenv import load_dotenv
import os

load_dotenv()

TRADING_PAIRS = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "AVAX/USDT"]  # Add or remove as needed

while True:
    for symbol in TRADING_PAIRS:
        price_data = fetch_kucoin_data(symbol)
        if not price_data:
            continue

        cvd = compute_cvd(price_data)
        
        trap_signal = cvd.get("trap")
        score = cvd.get("score")

        if trap_signal:
            log_signal(symbol, trap_signal, score)
            send_alert(symbol, trap_signal, score)

    time.sleep(60)  # Run every 60 seconds
