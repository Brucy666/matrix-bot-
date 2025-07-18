# delta_spike_engine.py

def detect_delta_spike(candle_data):
    """
    Detects delta spikes based on sudden volume surges in a single candle.

    Parameters:
        candle_data (dict): A dictionary with keys like:
            - 'delta': net delta of the candle (buy volume - sell volume)
            - 'volume': total volume of the candle
            - 'timestamp': candle timestamp

    Returns:
        dict: {
            'spike_detected': bool,
            'delta_value': float,
            'volume': float,
            'confidence': float
        }
    """

    delta = candle_data.get("delta", 0)
    volume = candle_data.get("volume", 1)
    timestamp = candle_data.get("timestamp", "N/A")

    # Simple spike logic: delta > X and volume > Y
    SPIKE_DELTA_THRESHOLD = 250000
    SPIKE_VOLUME_THRESHOLD = 1000000

    spike_detected = delta > SPIKE_DELTA_THRESHOLD and volume > SPIKE_VOLUME_THRESHOLD
    confidence = min(delta / SPIKE_DELTA_THRESHOLD, 2.0) if spike_detected else 0.0

    return {
        "spike_detected": spike_detected,
        "delta_value": delta,
        "volume": volume,
        "confidence": round(confidence, 2),
        "timestamp": timestamp
    }
