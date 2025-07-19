# gpt_money_flow.py
# AI-native money flow engine for Matrix Bot

import numpy as np

def calculate_gpt_money_flow(price: float, vwap: float, volume: float, rsi_slope: float = 0.0, spoof_ratio: float = 1.0):
    try:
        # 1. Base directional flow = price relation to VWAP * volume
        raw_flow = (price - vwap) * volume

        # 2. Normalize to [-1, +1] range
        norm_flow = np.tanh(raw_flow / 100000.0)

        # 3. Adjust with spoof pressure & RSI slope (momentum confirmation)
        spoof_adjust = min(max(spoof_ratio - 1.0, -1), 2) * 0.4  # range ~[-0.4, +0.8]
        rsi_adjust = np.tanh(rsi_slope / 5.0) * 0.6              # range ~[-0.6, +0.6]

        flow_score = norm_flow + spoof_adjust + rsi_adjust
        flow_score = round(max(min(flow_score, 1), -1), 3)

        if flow_score > 0.3:
            label = "Accumulation"
        elif flow_score < -0.3:
            label = "Distribution"
        else:
            label = "Neutral"

        return {
            "flow_score": flow_score,
            "label": label,
            "raw_flow": raw_flow,
            "adjusted_by": {
                "spoof": round(spoof_adjust, 3),
                "rsi": round(rsi_adjust, 3)
            }
        }

    except Exception as e:
        return {"flow_score": 0, "label": "Error", "error": str(e)}


# 🔁 Test Block
if __name__ == "__main__":
    test = calculate_gpt_money_flow(
        price=58250,
        vwap=58100,
        volume=1200000,
        rsi_slope=3.5,
        spoof_ratio=1.8
    )
    print("[MONEY FLOW TEST]", test)
