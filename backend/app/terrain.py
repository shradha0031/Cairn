"""Terrain calculations for the small Jezero demo area."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TerrainGrid:
    """Derived terrain arrays used by routing and safety calculations."""

    elevation_m: np.ndarray
    slope_degrees: np.ndarray
    hazard_cost: np.ndarray
    blocked: np.ndarray


def compute_slope_degrees(elevation_m: np.ndarray, cell_size_m: float = 10.0) -> np.ndarray:
    """Calculate slope angle from an elevation grid using finite differences.

    ``np.gradient`` keeps the calculation simple and deterministic for the demo.
    Edge cells use one-sided differences, while interior cells use centered
    differences. The resulting gradient is converted from rise/run to degrees.
    """

    if elevation_m.ndim != 2:
        raise ValueError("elevation_m must be a two-dimensional array")
    if cell_size_m <= 0:
        raise ValueError("cell_size_m must be positive")

    gradient_y, gradient_x = np.gradient(elevation_m, cell_size_m, cell_size_m)
    rise_over_run = np.hypot(gradient_x, gradient_y)
    return np.degrees(np.arctan(rise_over_run))


def build_hazard_grid(
    elevation_m: np.ndarray,
    terrain_units: np.ndarray | None = None,
    *,
    cell_size_m: float = 10.0,
    maximum_walkable_slope_degrees: float = 25.0,
    loose_ground_penalty: float = 3.0,
) -> TerrainGrid:
    """Build the cost and blocked-cell arrays used by a route planner.

    Higher slopes increase travel cost, while a terrain-unit value of ``1``
    represents loose ground and adds a penalty. Cells above the walkable slope
    are marked blocked with infinite cost instead of being silently traversed.
    """

    if maximum_walkable_slope_degrees <= 0:
        raise ValueError("maximum_walkable_slope_degrees must be positive")
    if loose_ground_penalty < 0:
        raise ValueError("loose_ground_penalty cannot be negative")

    slope_degrees = compute_slope_degrees(elevation_m, cell_size_m)
    if terrain_units is None:
        terrain_units = np.zeros_like(elevation_m, dtype=np.int8)
    if terrain_units.shape != elevation_m.shape:
        raise ValueError("terrain_units must match elevation_m shape")

    slope_factor = 1.0 + np.square(slope_degrees / maximum_walkable_slope_degrees)
    loose_ground_factor = np.where(terrain_units == 1, loose_ground_penalty, 0.0)
    hazard_cost = slope_factor + loose_ground_factor
    blocked = slope_degrees > maximum_walkable_slope_degrees
    hazard_cost = np.where(blocked, np.inf, hazard_cost)

    return TerrainGrid(
        elevation_m=elevation_m,
        slope_degrees=slope_degrees,
        hazard_cost=hazard_cost,
        blocked=blocked,
    )


def create_synthetic_elevation(rows: int = 100, columns: int = 160) -> np.ndarray:
    """Create a deterministic, clearly synthetic Jezero-like elevation surface."""

    if rows < 3 or columns < 3:
        raise ValueError("the synthetic grid needs at least 3 rows and columns")

    y, x = np.mgrid[0:rows, 0:columns]
    center_x, center_y = columns * 0.52, rows * 0.50
    distance = np.sqrt(((x - center_x) / columns) ** 2 + ((y - center_y) / rows) ** 2)
    crater_rim = 95.0 * np.exp(-((distance - 0.34) ** 2) / 0.006)
    floor = -18.0 * np.exp(-(distance**2) / 0.10)
    delta = 13.0 * np.exp(-(((x - columns * 0.67) / columns) ** 2 + ((y - rows * 0.42) / rows) ** 2) / 0.018)
    gentle_tilt = 8.0 * (x / columns) + 4.0 * (y / rows)
    return 1800.0 + crater_rim + floor + delta + gentle_tilt
