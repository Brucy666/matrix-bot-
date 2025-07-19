# gpt_money_flow.py

def calculate_gpt_money_flow(price, vwap, volume, rsi_slope, spoof_ratio):
    try:
        flow_score = 0
        reasons = []

        # Price above VWAP
        if price > vwap:
            flow_score += 1
            reasons.append("Above VWAP")
        elif price < vwap:
            flow_score += 0.5
            reasons.append("Below VWAP")

        # Volume strength
        if volume > 1_000_000:
            flow_score += 1
            reasons.append("High Volume")
        elif volume > 500_000:
            flow_score += 0.5
            reasons.append("Moderate Volume")

        # RSI slope strength
        if abs(rsi_slope) > 3.0:
            flow_score += 1
            reasons.append("Strong RSI Slope")
        elif abs(rsi_slope) > 1.5:
            flow_score += 0.5
            reasons.append("Mild RSI Slope")

        # Spoof pressure
        if spoof_ratio > 2.0:
            flow_score += 1
            reasons.append("Heavy Spoofing")
        elif spoof_ratio > 1.3:
            flow_score += 0.5
            reasons.append("Spoof Pressure")

        # Bias
        bias = "Above" if price > vwap else "Below"

        return {
            "money_flow_score": round(flow_score, 2),
            "bias": bias,
            "reason": ", ".join(reasons)
        }

    except Exception as e:
        return {"error": str(e)}
