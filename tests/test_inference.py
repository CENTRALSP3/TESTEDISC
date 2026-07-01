import json
from fastapi.testclient import TestClient
from api.main import app
from api.inference import build_context, evaluate_condition, infer_profile

client = TestClient(app)


def test_condition_parser_no_eval():
    ctx = build_context(
        {"D": 7, "I": 2, "S": 1, "C": 0},
        {"D": 2, "I": 2, "S": 1, "C": 0},
    )
    assert evaluate_condition("D_natural > 5", ctx)
    assert evaluate_condition("D_adapted < D_natural - 4", ctx)
    assert evaluate_condition("D_diff == 5", ctx)


def test_infer_suppression_rule():
    payload = {
        "natural": {"D": 8, "I": 1, "S": 0, "C": 0},
        "adapted": {"D": 2, "I": 1, "S": 0, "C": 0},
    }
    response = client.post("/infer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "RULE_SUPPRESS_D" in data["matched_rules"]
    assert data["confidence"] >= 0.85
    assert "Supressão" in data["interpretation"]


def test_infer_blend_di():
    payload = {
        "natural": {"D": 6, "I": 5, "S": 0, "C": -1},
        "adapted": {"D": 6, "I": 5, "S": 0, "C": -1},
    }
    response = client.post("/infer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "RULE_BLEND_DI" in data["matched_rules"]


def test_responses_and_analytics():
    payload = {
        "session_id": "test-session-001",
        "block": "natural",
        "question_id": "n01",
        "most_factor": "D",
        "least_factor": "C",
    }
    save = client.post("/responses", json=payload)
    assert save.status_code == 200
    assert save.json()["saved"] == 1

    analytics = client.get("/analytics")
    assert analytics.status_code == 200
    assert analytics.json()["total_responses"] >= 1