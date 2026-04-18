import heapq
from app.db.store import VENUE_GRAPH, current_counts

def calculate_edge_weight(distance: float, neighbor_zone: str) -> float:
    """
    Calculates the effective "cost" to travel an edge.
    Cost = distance + (crowd_penalty)
    A highly crowded zone adds artificial distance, making it less attractive.
    """
    crowd = current_counts.get(neighbor_zone, 0)
    
    # If the crowd is dangerously high, we consider the zone impassable (closed).
    if crowd >= 5000:
        return float('inf')

    # Apply a congestion penalty, but cap it so routing doesn't break
    # E.g., every 10 people adds 5 "units" of cost
    raw_penalty = (crowd / 10.0) * 5.0
    MAX_PENALTY = 300.0  # Cap to prevent absurdly long detours
    
    crowd_penalty = min(raw_penalty, MAX_PENALTY)
    return distance + crowd_penalty

def find_optimal_route(start: str, end: str):
    """
    Finds the shortest and least crowded path using Dijkstra's algorithm.
    """
    if start not in VENUE_GRAPH or end not in VENUE_GRAPH:
        raise ValueError("Invalid start or end zone")

    # Priority queue: (total_cost, current_node, path)
    queue = [(0.0, start, [start])]
    visited = set()

    while queue:
        cost, current, path = heapq.heappop(queue)

        if current == end:
            # Base assumption: 1 "unit" of cost roughly equals 1 second of walking
            estimated_time_minutes = cost / 60.0
            return {
                "path": path,
                "estimated_time_minutes": round(estimated_time_minutes, 2),
                "total_distance": round(cost, 2)
            }

        if current in visited:
            continue
        visited.add(current)

        for neighbor, distance in VENUE_GRAPH.get(current, {}).items():
            if neighbor not in visited:
                weight = calculate_edge_weight(distance, neighbor)
                
                # If weight is infinity, the zone is considered impassable/closed
                if weight == float('inf'):
                    continue
                    
                heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))

    return None # No path found (this gracefully bubbles up as a 404 in the API)
