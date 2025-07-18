# sniper_tools/sniper_confluence_score.py

def calculate_confluence_score(data):
    """
    Takes booleans from various engines and calculates a confluence score.
    """
    score = 0
    tags = []

    if data.get("cvd_divergence"):
        score += 1
        tags.append(data["cvd_divergence"])

    if data.get("poc_wick"):
        score += 1
        tags.append("POC Wick")

    if data.get("heatmap_sweep"):
        score += 1
        tags.append("Heatmap Sweep")

    if data.get("vwap_rejection"):
        score += 1
        tags.append("VWAP Rejection")

    return {"confluence_score": score, "tags": tags}
