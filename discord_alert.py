# discord_alert.py

import requests
import os
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_TRADE_WEBHOOK") or "https://discord.com/api/webhooks/1395380527938404363/e7RT8fXbH14NuInl0x-Z3uy111KjRZ78JcOkdHLmlnWZiwTfBQedGg43p3FpJ9ZSU3Xg"

def format_discord_alert(trade):
    color = 0x00ffae if trade["bias"].lower() == "above" else 0xff5555

    return {
        "username": "QuickStrike Bot",
        "embeds": [
            {
                "title": "🎯 Sniper Trade Executed",
                "color": color,
                "fields": [
                    {"name": "Token", "value": f"`{trade.get('symbol')}`", "inline": True},
                    {"name": "Exchange", "value": f"{trade.get('exchange')}", "inline": True},
                    {"name": "Bias", "value": f"{trade.get('bias')}", "inline": True},
                    {"name": "Spoof Ratio", "value": f"🔴 `{trade.get('spoof_ratio')}`", "inline": True},
                    {"name": "Trap Type", "value": f"{trade.get('trap_type')}", "inline": True},
                    {"name": "RSI", "value": f"{trade.get('rsi_status')}", "inline": True},
                    {"name": "VWAP / V Setup", "value": f"{trade.get('vsplit_score')}", "inline": True},
                    {"name": "Confidence", "value": f"{trade.get('confidence')}/10", "inline": True},
                    {"name": "Timestamp", "value": f"`{trade.get('timestamp')}`", "inline": False},
                ],
                "footer": {"text": "QuickStrike Sniper Feed"}
            }
        ]
    }

def send_discord_alert(trade_data):
    if not DISCORD_WEBHOOK:
        print("[!] Missing DISCORD_TRADE_WEBHOOK")
        return

    data = format_discord_alert(trade_data)

    try:
        response = requests.post(DISCORD_WEBHOOK, json=data)
        print(f"[Discord] Status Code: {response.status_code}")
        if response.status_code not in [200, 204]:
            print(f"[Discord] ERROR: {response.text}")
    except Exception as e:
        print(f"[!] Discord alert exception: {e}")
        
