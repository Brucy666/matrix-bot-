# discord_alert.py
import requests
import os
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_TRADE_WEBHOOK")  # Or hardcode for local test

def format_discord_alert(trade):
    return {
        "username": "QuickStrike Bot",
        "embeds": [
            {
                "title": "🎯 Sniper Trade Executed",
                "color": 0xff5555 if trade.get("exchange") == "Binance" else 0x00ffae,
                "fields": [
                    {"name": "Symbol", "value": f"`{trade.get('symbol', 'N/A')}`", "inline": True},
                    {"name": "Exchange", "value": f"`{trade.get('exchange', 'N/A')}`", "inline": True},
                    {"name": "Entry Price", "value": f"`{trade.get('entry_price', 0):.2f}`", "inline": True},
                    {"name": "VWAP", "value": f"`{trade.get('vwap', 0):.2f}`", "inline": True},
                    {"name": "RSI", "value": f"`{trade.get('rsi', 0):.2f}`", "inline": True},
                    {"name": "Score", "value": f"`{trade.get('score', 0)}`", "inline": True},
                    {"name": "Timestamp", "value": f"`{trade.get('timestamp', 'N/A')}`", "inline": False},
                ],
                "footer": {"text": "Matrix Sniper Alert"}
            }
        ]
    }

def send_discord_alert(trade):
    if not DISCORD_WEBHOOK:
        print("[!] DISCORD_WEBHOOK not set")
        return

    data = format_discord_alert(trade)
    try:
        response = requests.post(DISCORD_WEBHOOK, json=data)
        if response.status_code == 204:
            print("[✓] Discord alert sent.")
        else:
            print(f"[!] Discord alert failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"[!] Discord alert error: {e}")
