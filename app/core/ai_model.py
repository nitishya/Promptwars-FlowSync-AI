import time
from app.db.store import historical_counts, current_counts

def predict_congestion(zone: str) -> dict:
    """
    Predicts the congestion in a zone for the next 10 minutes using a simple moving average.
    Ignores data that is older than 15 minutes to prevent predicting based on stale data.
    """
    history = historical_counts[zone]
    now = time.time()
    
    # Filter out entries older than 15 minutes (900 seconds)
    valid_history = [entry for entry in history if now - entry[0] < 900]
    
    if len(valid_history) < 2:
        # No recent history, assume current count will remain stable
        current = current_counts.get(zone, 0)
        return {"predicted_count": current, "trend": "Stable"}

    counts = [entry[1] for entry in valid_history]
    
    # Simple moving average of the valid recent entries
    avg = sum(counts) / len(counts)
    
    # Simple trend detection based on the valid history
    half_point = max(1, len(counts) // 2)
    recent_avg = sum(counts[-half_point:]) / half_point
    older_avg = sum(counts[:half_point]) / half_point
    
    trend = "Stable"
    if recent_avg > older_avg * 1.1: # 10% increase
        trend = "Increasing"
    elif recent_avg < older_avg * 0.9: # 10% decrease
        trend = "Decreasing"

    # Prediction formula: base it on recent avg + a factor of trend
    prediction = int(recent_avg)
    if trend == "Increasing":
        prediction = int(recent_avg * 1.2) # Predict 20% growth over 10 mins
    elif trend == "Decreasing":
        prediction = int(recent_avg * 0.8)

    return {"predicted_count": max(0, prediction), "trend": trend}

def estimate_wait_time(zone: str) -> dict:
    """
    Estimates the wait time based on Little's Law or simple arrival/service rate logic.
    Assume Food Court processes 10 people per minute.
    Assume Restrooms process 15 people per minute.
    """
    people = current_counts.get(zone, 0)
    
    if zone == "Food Court":
        service_rate_per_minute = 10.0
        max_queue_capacity = 600
    elif zone == "Restrooms":
        service_rate_per_minute = 15.0
        max_queue_capacity = 200
    else:
        # Refuse to calculate wait times for non-service areas
        raise ValueError(f"Queue estimation is not supported for non-service zone: {zone}")

    # Cap the theoretical queue size to max physical capacity
    effective_people = min(people, max_queue_capacity)
    
    # Wait time = L / lambda (People / processing rate)
    wait_time = effective_people / service_rate_per_minute
    
    return {
        "zone": zone,
        "estimated_wait_time_minutes": round(wait_time, 2),
        "people_in_queue": people,
        "is_at_capacity": people >= max_queue_capacity
    }
