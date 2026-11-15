from app.stops import ALL_STOPS, SCIENCE_STOPS


def test_catalog_contains_science_and_emergency_stops() -> None:
    assert len(SCIENCE_STOPS) == 3
    assert len(ALL_STOPS) == 6
    assert {stop.stop_type for stop in ALL_STOPS} == {"science", "emergency"}


def test_unverified_photo_links_are_not_invented() -> None:
    assert SCIENCE_STOPS[0].photo_url is not None
    assert SCIENCE_STOPS[0].photo_status.startswith("NASA Perseverance")
    assert all(stop.photo_url is None for stop in SCIENCE_STOPS[1:])
    assert all(stop.photo_status == "pending verification" for stop in SCIENCE_STOPS[1:])
