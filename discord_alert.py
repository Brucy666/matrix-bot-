
import requests
from datetime import datetime

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1395380527938404363/e7RT8fXbH14NuInl0x-Z3uy111KjRZ78JcOkdHLmlnWZiwTfBQedGg43p3FpJ9ZSU3Xg"

def format_discord_alert(trade_data):
    symbol = trade_data.get("symbol", "N/A")
    exchange = trade_data.get("exchange", "Unknown")
    score = trade_data.get("score", 0)
    spoof = trade_data.get("spoof_ratio", 0)
    bias = trade_data.get("bias", "unknown").capitalize()
    trap_type = trade_data.get("trap_type", "Unclassified")
    rsi_status = trade_data.get("rsi_status", "None")
    confidence = trade_data.get("confidence", 0)
    vsetup = trade_data.get("vsplit_score", "None")
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    emoji = "📉" if bias == "Below" else "📈"
    spoof_emoji = "🟡" if spoof < 0.3 else "🟠" if spoof < 0.6 else "🔴"
    confidence_emoji = "🧠" if confidence >= 8 else "⚠️" if confidence >= 5 else "❓"
    rsi_emoji = "💥" if "split" in rsi_status.lower() else "🌀" if "collapse" in rsi_status.lower() else "📊"
    v_emoji = "🔵" if "vwap" in str(vsetup).lower() else "🟣" if "split" in str(vsetup).lower() else "❌"

    return {
        "username": "QuickStrike Bot",
        "embeds": [
            {
                "title": f"🎯 Sniper Trade Executed",
                "color": 0x00ffae if bias == "Above" else 0xff5555,
                "fields": [
                    {"name": "Token", "value": f"`{symbol}`", "inline": True},
                    {"name": "Exchange", "value": f"`{exchange}`", "inline": True},
                    {"name": "Bias", "value": f"{emoji} `{bias}`", "inline": True},
                    {"name": "Spoof Ratio", "value": f"{spoof_emoji} `{spoof:.3f}`", "inline": True},
                    {"name": "Trap Type", "value": f"`{trap_type}`", "inline": True},
                    {"name": "RSI", "value": f"{rsi_emoji} `{rsi_status}`", "inline": True},
                    {"name": "VWAP / V Setup", "value": f"{v_emoji} `{vsetup}`", "inline": True},
                    {"name": "Confidence", "value": f"{confidence_emoji} `{confidence}/10`", "inline": True},
                    {"name": "Timestamp", "value": f"`{timestamp}`", "inline": False}
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
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload, headers=headers)
        if response.status_code not in [204, 200]:
            print(f"[!] Discord alert failed: {response.status_code} | {response.text}")
        else:
            print("[✓] Discord alert sent.")
    except Exception as e:
        print(f"[!] Discord alert error: {e}")
