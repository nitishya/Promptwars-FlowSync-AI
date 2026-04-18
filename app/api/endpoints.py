import time
from collections import defaultdict
from fastapi import APIRouter, HTTPException, Request
from typing import List
from app.models.schemas import LocationData, ZoneDensity, HeatmapResponse, PredictionResponse, RouteRequest, RouteResponse, QueueEstimation
from app.db.store import current_counts, ZONES
from app.core.ai_model import predict_congestion, estimate_wait_time
from app.core.pathfinding import find_optimal_route

router = APIRouter()

# Rate limiting store: IP -> [window_start_timestamp, request_count]
rate_limits = defaultdict(lambda: [0.0, 0])
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 100  # max requests per window per IP

@router.post("/crowd-data", status_code=201)
async def receive_crowd_data(data: LocationData, request: Request):
    """
    Ingest simulated user location data.
    Updates the current density of the reported zone.
    Includes rate limiting to prevent spam.
    """
    client_ip = request.client.host
    now = time.time()
    
    # Enforce Rate Limit
    if now - rate_limits[client_ip][0] > RATE_LIMIT_WINDOW:
        rate_limits[client_ip] = [now, 1]
    else:
        if rate_limits[client_ip][1] >= RATE_LIMIT_MAX_REQUESTS:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Too many requests.")
        rate_limits[client_ip][1] += 1

    if data.zone not in ZONES:
        raise HTTPException(status_code=400, detail=f"Invalid zone. Must be one of: {', '.join(ZONES)}")
    
    current_counts[data.zone] += 1
    return {"message": "Data recorded successfully", "current_zone_count": current_counts[data.zone]}

@router.get("/heatmap", response_model=HeatmapResponse)
async def get_heatmap():
    """
    Returns the current crowd density across all zones.
    """
    zones_data = []
    for zone in ZONES:
        count = current_counts.get(zone, 0)
        
        # Determine density level based on arbitrary thresholds for simulation
        if count < 50:
            level = "Low"
        elif count < 150:
            level = "Medium"
        else:
            level = "High"
            
        zones_data.append(ZoneDensity(zone=zone, count=count, density_level=level))
        
    return HeatmapResponse(timestamp=time.time(), zones=zones_data)

@router.get("/predict", response_model=List[PredictionResponse])
async def get_prediction():
    """
    Returns predicted crowd congestion for the next 10 minutes for all zones.
    """
    predictions = []
    for zone in ZONES:
        pred_data = predict_congestion(zone)
        predictions.append(
            PredictionResponse(
                zone=zone, 
                predicted_count=pred_data["predicted_count"], 
                trend=pred_data["trend"]
            )
        )
    return predictions

@router.post("/route", response_model=RouteResponse)
async def get_route(request: RouteRequest):
    """
    Suggests the least crowded path between two points.
    Using a POST with body or GET with query params is fine; we'll use POST for cleaner JSON body.
    """
    if request.start_zone not in ZONES or request.end_zone not in ZONES:
        raise HTTPException(status_code=400, detail="Invalid start or end zone.")
        
    if request.start_zone == request.end_zone:
        return RouteResponse(path=[request.start_zone], estimated_time_minutes=0.0, total_distance=0.0)

    route_data = find_optimal_route(request.start_zone, request.end_zone)
    if not route_data:
        raise HTTPException(status_code=404, detail="No route found between these zones.")
        
    return RouteResponse(**route_data)

@router.get("/queue", response_model=List[QueueEstimation])
async def get_queue_estimates():
    """
    Returns estimated waiting times at service areas (Food Court, Restrooms).
    """
    service_zones = ["Food Court", "Restrooms"]
    estimates = []
    for zone in service_zones:
        estimates.append(QueueEstimation(**estimate_wait_time(zone)))
    return estimates
