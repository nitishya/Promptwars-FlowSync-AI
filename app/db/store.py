from typing import Dict, List, Tuple
from collections import deque
import time

# Venue zones
ZONES = ["Gate A", "Gate B", "Food Court", "Parking", "Main Stand", "Restrooms"]

# Graph representation: zone -> {neighbor_zone: distance}
VENUE_GRAPH: Dict[str, Dict[str, float]] = {
    "Gate A": {"Food Court": 50, "Main Stand": 100, "Parking": 200},
    "Gate B": {"Restrooms": 30, "Main Stand": 80, "Parking": 250},
    "Food Court": {"Gate A": 50, "Main Stand": 40, "Restrooms": 20},
    "Parking": {"Gate A": 200, "Gate B": 250},
    "Main Stand": {"Gate A": 100, "Gate B": 80, "Food Court": 40, "Restrooms": 60},
    "Restrooms": {"Gate B": 30, "Food Court": 20, "Main Stand": 60}
}

# Current state: count of people in each zone
current_counts: Dict[str, int] = {zone: 0 for zone in ZONES}

# Historical data for moving average prediction: zone -> deque of recent counts (timestamp, count)
HISTORY_LIMIT = 60 # Store up to 60 snapshots
historical_counts: Dict[str, deque] = {zone: deque(maxlen=HISTORY_LIMIT) for zone in ZONES}

def record_snapshot():
    """Records the current counts into the historical deque for all zones"""
    now = time.time()
    for zone in ZONES:
        historical_counts[zone].append((now, current_counts[zone]))
