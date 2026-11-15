from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_identifies_jezero() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "site": "Jezero Crater"}


def test_layers_are_marked_synthetic() -> None:
    response = client.get("/layers")

    assert response.status_code == 200
    assert response.json()["synthetic_data"] is True
    assert response.json()["real_layers"] == ["base imagery"]
    assert response.json()["synthetic_layers"] == ["elevation", "slope", "terrain units"]


def test_routes_returns_three_candidates() -> None:
    response = client.post("/routes", json={"start": [41, 55], "end": [66, 104]})

    assert response.status_code == 200
    body = response.json()
    assert body["synthetic_data"] is True
    assert [route["route_id"] for route in body["routes"]] == ["safest", "shortest", "science"]


def test_safety_returns_turn_back_assessment() -> None:
    response = client.post("/safety", json={"route_id": "safest", "progress": 0.5, "available_minutes": 30})

    assert response.status_code == 200
    body = response.json()
    assert body["alert_level"] == "AMBER"
    assert body["nearest_emergency_stop"]["name"] in {"Habitat", "Delta shelter"}


def test_briefing_endpoint_uses_template_without_llm() -> None:
    response = client.post("/briefing", json={"facts": {"alert_level": "GREEN", "route_name": "Safest route"}})

    assert response.status_code == 200
    assert response.json()["source"] == "template"
    assert "GREEN" in response.json()["summary"]
