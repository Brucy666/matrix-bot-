# sniper_tools/heatmap_sweep_engine.py

def detect_heatmap_sweep(price, heatmap_clusters):
    """
    Detects if price has swept a major liquidity zone in the heatmap clusters
    """
    sweep_zones = [cluster for cluster in heatmap_clusters if abs(price - cluster) < 5]

    if sweep_zones:
        return {"sweep": True, "zone": sweep_zones[0]}
    return {"sweep": False, "zone": None}
