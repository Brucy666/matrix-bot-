# discord_alert.py

import requests
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1395380527938404363/e7RT8fXbH14NuInl0x-Z3uy111KjRZ78JcOkdHLmlnWZiwTfBQedGg43p3FpJ9ZSU3Xg"

def build_embed(trap_data):
    # Format the timestamp
    timestamp = datetime.utcnow().isoformat()

    # Build the Discord embed payload
    embed = {
        "title": "🎯 Sniper Trade Executed",
        "color": 15158332 if trap_data["score"] < 4 else 3066993,  # Red if low score, green if high
        "fields": [
            {"name": "Symbol", "value": trap_data["symbol"], "inline": True},
            {"name": "Exchange", "value": trap_data["exchange"], "inline": True},
            {"name": "Entry Price", "value": str(trap_data["entry_price"]), "inline": True},
            {"name": "VWAP", "value": str(trap_data.get("vwap", "N/A")), "inline": True},
            {"name": "RSI", "value": str(trap_data.get("rsi", "N/A")), "inline": True},
            {"name": "Score", "value": str(trap_data["score"]), "inline": True},
            {"name": "Trap Type", "value": trap_data.get("trap_type", "N/A"), "inline": True},
            {"name": "Bias", "value": trap_data.get("bias", "Unknown"), "inline": True},
            {"name": "VWAP / V Setup", "value": trap_data.get("vsplit_score", "None"), "inline": True},
            {"name": "RSI", "value": trap_data.get("rsi_status", "None"), "inline": True},
            {"name": "Spoof Ratio", "value": str(trap_data.get("spoof_ratio", 0)), "inline": True},
            {"name": "Confidence", "value": f"{trap_data['confidence']}/10", "inline": True},
        ],
        "footer": {
            "text": "Matrix Sniper Feed"
        },
        "timestamp": timestamp
    }
    return embed

def send_discord_alert(trap_data):
    embed = build_embed(trap_data)
    payload = {
        "content": None,
        "embeds": [embed],
        "username": "Matrix Sniper Bot"
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("✅ Discord alert sent successfully.")
        else:
            print(f"[!] Discord alert failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[!] Discord alert exception: {e}")
