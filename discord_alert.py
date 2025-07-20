import os
import requests
import json

def send_discord_alert(trade_data):
    webhook_url = os.getenv("DISCORD_WEBHOOK")

    if not webhook_url:
        print("[Discord] ❌ DISCORD_WEBHOOK not set.")
        return

    try:
        # Extract fallback values
        symbol = trade_data.get("symbol", "Unknown")
        exchange = trade_data.get("exchange", "Unknown")
        entry_price = trade_data.get("entry_price", "N/A")
        vwap = trade_data.get("vwap", "N/A")
        rsi = trade_data.get("rsi", "N/A")
        score = trade_data.get("score", 0)
        timestamp = trade_data.get("timestamp", "N/A")

        # Construct fields
        embed = {
            "title": "🎯 Sniper Trade Executed",
            "color": 15158332,
            "fields": [
                {"name": "Symbol", "value": str(symbol), "inline": True},
                {"name": "Exchange", "value": str(exchange), "inline": True},
                {"name": "Entry Price", "value": str(entry_price), "inline": True},
                {"name": "VWAP", "value": str(vwap), "inline": True},
                {"name": "RSI", "value": str(rsi), "inline": True},
                {"name": "Score", "value": str(score), "inline": True},
                {"name": "Timestamp", "value": str(timestamp), "inline": False}
            ],
            "footer": {"text": "Matrix Sniper Alert"}
        }

        response = requests.post(webhook_url, json={"embeds": [embed]})

        if response.status_code == 204:
            print("[✓] Discord alert sent.")
        else:
            print(f"[Discord] Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"[Discord] Alert failure: {e}")
