# sniper_tools/vwap_rejection_engine.py

def detect_vwap_rejection(price, vwap, previous_price):
    """
    Detects whether price has rejected from the VWAP level.
    """
    if previous_price < vwap and price > vwap:
        return {"rejection": True, "direction": "breakout up"}
    elif previous_price > vwap and price < vwap:
        return {"rejection": True, "direction": "rejection down"}
    return {"rejection": False, "direction": None}
