"""API schemas shared by the Cairn backend."""

from pydantic import BaseModel

from .config import Assumptions


class HealthResponse(BaseModel):
    status: str
    site: str


class LayersResponse(BaseModel):
    layers: list[str]
    synthetic_data: bool
    real_layers: list[str]
    synthetic_layers: list[str]


class AssumptionsResponse(BaseModel):
    assumptions: Assumptions


class RouteRequest(BaseModel):
    start: tuple[int, int]
    end: tuple[int, int]
    resources: dict[str, float] = {}
    weights: dict[str, float] = {}


class RouteSegmentResponse(BaseModel):
    rating: str
    reason: str
    path: list[tuple[int, int]]


class RouteResponse(BaseModel):
    route_id: str
    name: str
    path: list[tuple[int, int]]
    distance_m: float
    walking_time_minutes: float
    average_slope_degrees: float
    max_slope_degrees: float
    safety_rating: str
    science_value: int
    segments: list[RouteSegmentResponse]


class RoutesResponse(BaseModel):
    routes: list[RouteResponse]
    synthetic_data: bool


class SafetyRequest(BaseModel):
    route_id: str
    progress: float
    available_minutes: float | None = None


class EmergencyStopResponse(BaseModel):
    name: str
    stop_type: str
    point: tuple[int, int]


class SafetyResponse(BaseModel):
    route_id: str
    progress: float
    alert_level: str
    return_time_minutes: float
    return_need_minutes: float
    remaining_resources_minutes: float
    resource_buffer_minutes: float
    turn_back_progress: float
    turn_back_point: tuple[int, int]
    nearest_emergency_stop: EmergencyStopResponse
    message: str


class StopResponse(BaseModel):
    stop_id: str
    name: str
    stop_type: str
    point: tuple[int, int]
    safety_rating: str
    description: str
    photo_url: str | None
    photo_status: str


class StopsResponse(BaseModel):
    stops: list[StopResponse]
    synthetic_data: bool


class BriefingRequest(BaseModel):
    facts: dict[str, object]


class BriefingResponse(BaseModel):
    summary: str
    source: str
