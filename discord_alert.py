import requests
import os
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def format_matrix_alert(trade_data):
    symbol = trade_data.get("symbol", "Unknown")
    exchange = trade_data.get("exchange", "Unknown")
    entry_price = trade_data.get("entry_price", "?")
    vwap = trade_data.get("vwap", "?")
    rsi = trade_data.get("rsi", "?")
    score = trade_data.get("score", "?")
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return {
        "username": "Matrix Sniper Alert",
        "embeds": [
            {
                "title": "🎯 Sniper Trade Executed",
                "color": 0xff4f4f,
                "fields": [
                    {"name": "Symbol", "value": symbol, "inline": True},
                    {"name": "Exchange", "value": exchange, "inline": True},
                    {"name": "Entry Price", "value": str(entry_price), "inline": True},
                    {"name": "VWAP", "value": str(vwap), "inline": True},
                    {"name": "RSI", "value": str(rsi), "inline": True},
                    {"name": "Score", "value": str(score), "inline": True},
                    {"name": "Timestamp", "value": timestamp, "inline": False},
                ],
                "footer": {"text": "Matrix Sniper Alert"}
            }
        ]
    }

def send_discord_alert(trade_data):
    if not DISCORD_WEBHOOK:
        print("[!] DISCORD_WEBHOOK not set.")
        return

    data = format_matrix_alert(trade_data)
    try:
        response = requests.post(DISCORD_WEBHOOK, json=data)
        if response.status_code != 204:
            print(f"[!] Discord alert failed: {response.status_code}")
        else:
            print("[+] Discord alert sent successfully.")
    except Exception as e:
        print(f"[!] Discord alert error: {e}")
