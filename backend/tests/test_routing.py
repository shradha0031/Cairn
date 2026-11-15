import pytest

from app.routing import DEFAULT_END, DEFAULT_START, generate_candidate_routes


def test_generates_three_named_candidates() -> None:
    routes = generate_candidate_routes()

    assert [route.route_id for route in routes] == ["safest", "shortest", "science"]
    assert all(route.path[0] == DEFAULT_START for route in routes)
    assert all(route.path[-1] == DEFAULT_END for route in routes)


def test_routes_have_comparable_metrics_and_segments() -> None:
    routes = generate_candidate_routes()

    for route in routes:
        assert route.distance_m > 0
        assert route.walking_time_minutes > 0
        assert route.max_slope_degrees >= route.average_slope_degrees
        assert route.safety_rating in {"green", "blue", "black"}
        assert route.segments
        assert all(segment.rating in {"green", "blue", "black"} for segment in route.segments)


def test_rejects_points_outside_demo_grid() -> None:
    with pytest.raises(ValueError, match="100 x 160"):
        generate_candidate_routes(start=(100, 160))
