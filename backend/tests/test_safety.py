import pytest

from app.safety import assess_safety


def test_start_is_green_with_large_resource_reserve() -> None:
    assessment = assess_safety("safest", progress=0.0, available_minutes=30.0)

    assert assessment.alert_level == "GREEN"
    assert assessment.return_time_minutes == 0
    assert assessment.nearest_emergency_stop.name == "Habitat"


def test_progression_reaches_amber_then_red() -> None:
    amber = assess_safety("safest", progress=0.5, available_minutes=30.0)
    red = assess_safety("safest", progress=1.0, available_minutes=30.0)

    assert amber.alert_level == "AMBER"
    assert red.alert_level == "RED"
    assert red.return_need_minutes > red.remaining_resources_minutes


def test_invalid_safety_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="between 0 and 1"):
        assess_safety("safest", progress=1.1)
    with pytest.raises(ValueError, match="positive"):
        assess_safety("safest", progress=0.2, available_minutes=0)
