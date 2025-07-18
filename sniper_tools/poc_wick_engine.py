# sniper_tools/poc_wick_engine.py

def detect_poc_wick(wick_high, wick_low, poc_level):
    """
    EMERGENCY DEBUG MODE — log types and values, then force unwrap all inputs.
    """

    def unwrap(val):
        original = val
        depth = 0
        try:
            while isinstance(val, list):
                val = val[0]
                depth += 1
                if depth > 10:
                    raise ValueError("Too deeply nested.")
            return float(val)
        except Exception as e:
            print(f"[POC UNWRAP FAIL] {original} → {e}")
            return None

    # Unwrap and debug
    high = unwrap(wick_high)
    low = unwrap(wick_low)
    poc = unwrap(poc_level)

    print(f"[POC DEBUG] type(high)={type(high)}, type(low)={type(low)}, type(poc)={type(poc)}")
    print(f"[POC DEBUG] high={high}, low={low}, poc={poc}")

    if None in (high, low, poc):
        return "[POC Wick Error] Invalid input — could not unwrap."

    try:
        if high > poc and low < poc:
            return f"POC Wick Trap Detected near {round(poc, 2)}"
    except Exception as e:
        return f"[POC COMPARISON ERROR] {e}"

    return None
