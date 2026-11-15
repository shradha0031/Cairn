"""Least-cost route generation for the synthetic Jezero grid."""

from dataclasses import dataclass
from math import hypot
from typing import Literal

import numpy as np
from skimage.graph import route_through_array

from .config import ASSUMPTIONS
from .terrain import TerrainGrid, build_hazard_grid, create_synthetic_elevation

GridPoint = tuple[int, int]
RouteMode = Literal["safest", "shortest", "science"]
DEFAULT_START: GridPoint = (41, 55)
DEFAULT_END: GridPoint = (66, 104)
SCIENCE_STOP: GridPoint = (54, 88)


@dataclass(frozen=True)
class RouteSegment:
    """A contiguous section of a route with one safety rating."""

    rating: str
    reason: str
    path: list[GridPoint]


@dataclass(frozen=True)
class CandidateRoute:
    """Computed facts presented by the API and route comparison table."""

    route_id: str
    name: str
    path: list[GridPoint]
    distance_m: float
    walking_time_minutes: float
    average_slope_degrees: float
    max_slope_degrees: float
    safety_rating: str
    science_value: int
    segments: list[RouteSegment]


def load_demo_terrain() -> TerrainGrid:
    """Build the deterministic terrain grid used until verified data is available."""

    elevation = create_synthetic_elevation()
    terrain_units = np.zeros_like(elevation, dtype=np.int8)
    terrain_units[42:60, 75:104] = 1
    return build_hazard_grid(
        elevation,
        terrain_units,
        maximum_walkable_slope_degrees=ASSUMPTIONS.maximum_walkable_slope_degrees,
    )


def _validate_point(point: GridPoint, shape: tuple[int, int], name: str) -> None:
    """Reject points outside the local raster or inside blocked terrain."""

    row, column = point
    if not (0 <= row < shape[0] and 0 <= column < shape[1]):
        raise ValueError(f"{name} must be inside the 100 x 160 demo grid")


def _find_path(cost_grid: np.ndarray, start: GridPoint, end: GridPoint) -> list[GridPoint]:
    path, _ = route_through_array(
        cost_grid,
        start,
        end,
        fully_connected=True,
        geometric=True,
    )
    return [(int(row), int(column)) for row, column in path]


def _cost_grid(terrain: TerrainGrid, mode: RouteMode) -> np.ndarray:
    """Create a positive cost surface for one route strategy."""

    if mode == "shortest":
        return np.where(terrain.blocked, np.inf, 1.0)

    cost = terrain.hazard_cost.copy()
    if mode == "science":
        # Attract the science route toward the synthetic delta unit without
        # allowing the route to cross blocked cells or use negative costs.
        row, column = SCIENCE_STOP
        rows, columns = np.indices(cost.shape)
        distance = np.hypot(rows - row, columns - column)
        cost = np.maximum(0.25, cost - 1.2 * np.exp(-(distance**2) / 180.0))
    return cost


def _combine_paths(first: list[GridPoint], second: list[GridPoint]) -> list[GridPoint]:
    """Join two paths without duplicating their shared waypoint."""

    return first + second[1:]


def _rating(slope_degrees: float) -> str:
    if slope_degrees <= 8.0:
        return "green"
    if slope_degrees <= ASSUMPTIONS.maximum_walkable_slope_degrees:
        return "blue"
    return "black"


def _reason(rating: str, slope_degrees: float) -> str:
    if rating == "green":
        return f"Firm, gentle ground at {slope_degrees:.1f} degrees average slope."
    if rating == "blue":
        return f"Careful footing required at {slope_degrees:.1f} degrees average slope."
    return "Above the walkable slope limit; this segment is dangerous."


def _segments(path: list[GridPoint], slopes: np.ndarray) -> list[RouteSegment]:
    """Group adjacent path cells by their hiking-style safety rating."""

    segments: list[RouteSegment] = []
    current_rating: str | None = None
    current_path: list[GridPoint] = []
    for point in path:
        rating = _rating(float(slopes[point]))
        if current_rating is not None and rating != current_rating:
            mean_slope = float(np.mean([slopes[item] for item in current_path]))
            segments.append(RouteSegment(current_rating, _reason(current_rating, mean_slope), current_path))
            current_path = []
        current_rating = rating
        current_path.append(point)

    if current_rating is not None:
        mean_slope = float(np.mean([slopes[item] for item in current_path]))
        segments.append(RouteSegment(current_rating, _reason(current_rating, mean_slope), current_path))
    return segments


def _measure_route(path: list[GridPoint], terrain: TerrainGrid, route_id: str, name: str) -> CandidateRoute:
    """Calculate route metrics from the known path and terrain arrays."""

    slopes = np.array([terrain.slope_degrees[point] for point in path])
    distance_m = sum(hypot(row_b - row_a, column_b - column_a) * 10.0 for (row_a, column_a), (row_b, column_b) in zip(path, path[1:]))
    speed_m_per_minute = (ASSUMPTIONS.walking_speed_kmh * 1000.0 / 60.0) * ASSUMPTIONS.equipment_load_factor
    slope_adjustment = np.maximum(0.25, 1.0 - ASSUMPTIONS.slope_speed_penalty * slopes)
    walking_time_minutes = float(np.sum((distance_m / max(len(path) - 1, 1)) / (speed_m_per_minute * slope_adjustment)))
    average_slope = float(np.mean(slopes))
    maximum_slope = float(np.max(slopes))
    safety_rating = "green" if maximum_slope <= 8 else "blue" if maximum_slope <= 18 else "black"
    science_value = int(np.sum(np.array([hypot(row - SCIENCE_STOP[0], column - SCIENCE_STOP[1]) for row, column in path]) <= 8))
    return CandidateRoute(
        route_id=route_id,
        name=name,
        path=path,
        distance_m=round(distance_m, 1),
        walking_time_minutes=round(walking_time_minutes, 1),
        average_slope_degrees=round(average_slope, 1),
        max_slope_degrees=round(maximum_slope, 1),
        safety_rating=safety_rating,
        science_value=min(science_value, 100),
        segments=_segments(path, terrain.slope_degrees),
    )


def generate_candidate_routes(start: GridPoint = DEFAULT_START, end: GridPoint = DEFAULT_END) -> list[CandidateRoute]:
    """Generate safest, shortest, and science-focused candidates."""

    terrain = load_demo_terrain()
    _validate_point(start, terrain.elevation_m.shape, "start")
    _validate_point(end, terrain.elevation_m.shape, "end")
    if terrain.blocked[start] or terrain.blocked[end]:
        raise ValueError("start and end must be walkable cells")

    routes: list[CandidateRoute] = []
    for route_id, name, mode in (
        ("safest", "Safest route", "safest"),
        ("shortest", "Shortest route", "shortest"),
    ):
        path = _find_path(_cost_grid(terrain, mode), start, end)
        routes.append(_measure_route(path, terrain, route_id, name))

    science_path = _combine_paths(
        _find_path(_cost_grid(terrain, "science"), start, SCIENCE_STOP),
        _find_path(_cost_grid(terrain, "science"), SCIENCE_STOP, end),
    )
    routes.append(_measure_route(science_path, terrain, "science", "Science route"))
    return routes
