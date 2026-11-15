from app.briefing import create_briefing, template_briefing


def test_template_briefing_preserves_computed_numbers() -> None:
    summary = template_briefing({
        "route_name": "Safest route",
        "alert_level": "AMBER",
        "progress": 0.5,
        "return_need_minutes": 8.4,
        "remaining_resources_minutes": 23.0,
        "turn_back_progress": 0.47,
        "nearest_emergency_stop": "Habitat",
    })

    assert "AMBER" in summary
    assert "8.4 minutes" in summary
    assert "23.0 minutes" in summary
    assert "47%" in summary


def test_briefing_defaults_to_template_without_llm(monkeypatch) -> None:
    monkeypatch.delenv("CAIRN_LLM_ENDPOINT", raising=False)

    result = create_briefing({"alert_level": "GREEN"})

    assert result.source == "template"
    assert "GREEN" in result.summary
