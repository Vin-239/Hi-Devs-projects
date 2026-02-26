import numpy as np

# Compute trend direction based on slope of daily average sentiment.
# Input must be ordered chronologically.
    
def compute_trend(daily_sentiments: list[float]) -> str:
    
    if not daily_sentiments or len(daily_sentiments) < 2:
        return "Stable"

    x = np.arange(len(daily_sentiments))
    y = np.array(daily_sentiments)

    slope = np.polyfit(x, y, 1)[0]

    if slope > 0.05:
        return "Improving"
    elif slope < -0.05:
        return "Degrading"
    else:
        return "Stable"