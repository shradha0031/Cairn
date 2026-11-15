import numpy as np
import pytest

from app.terrain import build_hazard_grid, compute_slope_degrees, create_synthetic_elevation


def test_flat_elevation_has_zero_slope() -> None:
    elevation = np.full((4, 4), 100.0)

    slope = compute_slope_degrees(elevation)

    assert np.allclose(slope, 0.0)


def test_steep_cells_are_blocked() -> None:
    elevation = np.tile(np.arange(5, dtype=float) * 100.0, (5, 1))

    terrain = build_hazard_grid(elevation, maximum_walkable_slope_degrees=10.0)

    assert terrain.blocked.any()
    assert np.isinf(terrain.hazard_cost[terrain.blocked]).all()


def test_loose_ground_costs_more_than_firm_ground() -> None:
    elevation = np.full((4, 4), 100.0)
    terrain_units = np.zeros((4, 4), dtype=np.int8)
    terrain_units[2, 2] = 1

    terrain = build_hazard_grid(elevation, terrain_units)

    assert terrain.hazard_cost[2, 2] > terrain.hazard_cost[0, 0]


def test_synthetic_surface_is_reproducible() -> None:
    first = create_synthetic_elevation()
    second = create_synthetic_elevation()

    assert first.shape == (100, 160)
    assert np.array_equal(first, second)


def test_invalid_grid_dimensions_are_rejected() -> None:
    with pytest.raises(ValueError, match="two-dimensional"):
        compute_slope_degrees(np.ones(4))
