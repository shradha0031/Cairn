"""Return-safety calculations for a selected route."""

from dataclasses import dataclass
from math import hypot

from .config import ASSUMPTIONS
from .routing import CandidateRoute, GridPoint, generate_candidate_routes


@dataclass(frozen=True)
class EmergencyStop:
    """A location the crew can use during a return warning."""

    name: str
    stop_type: str
    point: GridPoint


@dataclass(frozen=True)
class SafetyAssessment:
    """Current return resources and the route's turn-back warning."""

    route_id: str
    progress: float
    alert_level: str
    return_time_minutes: float
    return_need_minutes: float
    remaining_resources_minutes: float
    resource_buffer_minutes: float
    turn_back_progress: float
    turn_back_point: GridPoint
    nearest_emergency_stop: EmergencyStop
    message: str


EMERGENCY_STOPS = (
    EmergencyStop("Habitat", "habitat", (41, 55)),
    EmergencyStop("Delta shelter", "shelter", (55, 80)),
)


def _route_for_id(route_id: str) -> CandidateRoute:
    routes = generate_candidate_routes()
    for route in routes:
        if route.route_id == route_id:
            return route
    raise ValueError(f"unknown route_id: {route_id}")


def _assessment_at_progress(route: CandidateRoute, progress: float, available_minutes: float) -> tuple[float, float, float, float]:
    """Return elapsed time, return need, remaining resources, and buffer."""

    outbound_time = route.walking_time_minutes * progress
    return_time = outbound_time
    return_need = return_time * ASSUMPTIONS.oxygen_consumption_rate_per_minute * (1 + ASSUMPTIONS.safety_margin)
    remaining = available_minutes - outbound_time * ASSUMPTIONS.oxygen_consumption_rate_per_minute
    return return_time, return_need, remaining, remaining - return_need


def _nearest_stop(point: GridPoint) -> EmergencyStop:
    return min(EMERGENCY_STOPS, key=lambda stop: hypot(point[0] - stop.point[0], point[1] - stop.point[1]))


def assess_safety(route_id: str, progress: float, available_minutes: float | None = None) -> SafetyAssessment:
    """Calculate the crew's return margin and earliest turn-back point."""

    if not 0 <= progress <= 1:
        raise ValueError("progress must be between 0 and 1")
    if available_minutes is not None and available_minutes <= 0:
        raise ValueError("available_minutes must be positive")

    route = _route_for_id(route_id)
    resource_budget = available_minutes if available_minutes is not None else ASSUMPTIONS.suit_oxygen_duration_minutes
    return_time, return_need, remaining, buffer = _assessment_at_progress(route, progress, resource_budget)

    turn_back_progress = 1.0
    for step in range(len(route.path)):
        candidate_progress = step / max(len(route.path) - 1, 1)
        _, _, _, candidate_buffer = _assessment_at_progress(route, candidate_progress, resource_budget)
        if candidate_buffer <= ASSUMPTIONS.return_threshold_minutes:
            turn_back_progress = candidate_progress
            break

    current_index = min(round(progress * (len(route.path) - 1)), len(route.path) - 1)
    current_point = route.path[current_index]
    turn_back_index = round(turn_back_progress * (len(route.path) - 1))
    turn_back_point = route.path[turn_back_index]

    if buffer <= 0:
        alert_level = "RED"
        message = "Turn back now or use the nearest emergency stop."
    elif buffer <= ASSUMPTIONS.return_threshold_minutes:
        alert_level = "AMBER"
        message = "Turn back soon to preserve the return reserve."
    else:
        alert_level = "GREEN"
        message = "Continue. Return reserve is comfortably above the threshold."

    return SafetyAssessment(
        route_id=route_id,
        progress=round(progress, 3),
        alert_level=alert_level,
        return_time_minutes=round(return_time, 1),
        return_need_minutes=round(return_need, 1),
        remaining_resources_minutes=round(remaining, 1),
        resource_buffer_minutes=round(buffer, 1),
        turn_back_progress=round(turn_back_progress, 3),
        turn_back_point=turn_back_point,
        nearest_emergency_stop=_nearest_stop(current_point),
        message=message,
    )
