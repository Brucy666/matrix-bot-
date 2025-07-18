# trap_journal.py

import csv
import os
from datetime import datetime

JOURNAL_FILE = "trap_journal.csv"

# Ensure the journal file exists with headers
if not os.path.exists(JOURNAL_FILE):
    with open(JOURNAL_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Symbol", "Score", "Reason", "Price", "Result"])

def log_trap(symbol, score, reason, price, result="pending"):
    with open(JOURNAL_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat(),
            symbol,
            score,
            reason,
            price,
            result
        ])
    print(f"[TrapJournal] Logged: {symbol} @ {price} | Score: {score} | {reason} -> {result}")

def read_traps():
    traps = []
    with open(JOURNAL_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            traps.append(row)
    return traps

if __name__ == "__main__":
    log_trap("BTC-USDT", 92, "RSI-V + VWAP confluence", 58250.12)
    print(read_traps()[-1])
