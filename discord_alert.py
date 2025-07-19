import requests
from datetime import datetime

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1395380527938404363/e7RT8fXbH14NuInl0x-Z3uy111KjRZ78JcOkdHLmlnWZiwTfBQedGg43p3FpJ9ZSU3Xg"

def format_discord_alert(trade):
    return {
        "username": "QuickStrike Bot",
        "embeds": [
            {
                "title": "🎯 Sniper Trade Executed",
                "color": 0xff5555 if trade.get("bias") == "Below" else 0x00ffae,
                "fields": [
                    {"name": "Token", "value": f"`{trade.get('symbol', 'Unknown')}`", "inline": True},
                    {"name": "Exchange", "value": f"{trade.get('exchange', 'N/A')}", "inline": True},
                    {"name": "Bias", "value": f"📉 `{trade.get('bias', 'Unknown')}`", "inline": True},
                    {"name": "Spoof Ratio", "value": f"🔴 `{trade.get('spoof_ratio', 0):.3f}`", "inline": True},
                    {"name": "Trap Type", "value": f"`{trade.get('trap_type', 'Unclassified')}`", "inline": True},
                    {"name": "RSI", "value": f"💥 `{trade.get('rsi_status', 'None')}`", "inline": True},
                    {"name": "VWAP / V Setup", "value": f"🔵 `{trade.get('vsplit_score', 'None')}`", "inline": True},
                    {"name": "Confidence", "value": f"❓ `{trade.get('confidence', 0)}/10`", "inline": True},
                    {"name": "Timestamp", "value": f"`{trade.get('timestamp', datetime.utcnow().isoformat())}`", "inline": False}
                ],
                "footer": {"text": "QuickStrike Sniper Feed"}
            }
        ]
    }

def send_discord_alert(trade_data):
    if not DISCORD_WEBHOOK:
        print("[!] Missing DISCORD_WEBHOOK")
        return

    payload = format_discord_alert(trade_data)
    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload)
        print(f"[Discord] Status Code: {response.status_code}")
        if response.status_code != 204:
            print("[Discord] Error response:", response.text)
    except Exception as e:
        print(f"[!] Discord alert exception: {e}")
