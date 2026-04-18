from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class LocationData(BaseModel):
    user_id: str
    zone: str
    timestamp: float

class ZoneDensity(BaseModel):
    zone: str
    count: int
    density_level: str  # "Low", "Medium", "High"

class HeatmapResponse(BaseModel):
    timestamp: float
    zones: List[ZoneDensity]

class PredictionResponse(BaseModel):
    zone: str
    predicted_count: int
    trend: str  # "Increasing", "Decreasing", "Stable"

class RouteRequest(BaseModel):
    start_zone: str
    end_zone: str

class RouteResponse(BaseModel):
    path: List[str]
    estimated_time_minutes: float
    total_distance: float

class QueueEstimation(BaseModel):
    zone: str
    estimated_wait_time_minutes: float
    people_in_queue: int
    is_at_capacity: bool = False
