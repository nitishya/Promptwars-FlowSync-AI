import asyncio
import random
from app.db.store import ZONES, current_counts, record_snapshot

async def run_simulation():
    """
    Background task to simulate realistic crowd movements.
    It periodically changes the counts in different zones and records history.
    """
    while True:
        # Simulate people moving around
        for zone in ZONES:
            # Random fluctuation: +/- 10% or +/- 5 people
            change = random.randint(-5, 5)
            # Add some logic for "surge" at gates or food court
            if zone == "Gate A" and random.random() > 0.8:
                change += random.randint(10, 30) # Surge of arrivals
            elif zone == "Food Court" and random.random() > 0.7:
                change += random.randint(5, 15)

            new_count = current_counts[zone] + change
            # Ensure it doesn't drop below 0
            current_counts[zone] = max(0, new_count)

        # Record this state in history
        record_snapshot()
        
        # Wait for 5 seconds before next tick
        await asyncio.sleep(5)
