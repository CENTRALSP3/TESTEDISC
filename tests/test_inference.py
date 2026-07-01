import json
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_infer_basic_rule():
    # Use scores that satisfy RULE_001 (D > 15 and C > 15)
    payload = {"D": 20, "I": 5, "S": 5, "C": 18}
    response = client.post("/infer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["interpretation"] == "Perfil extremamente lógico"
    assert data["confidence"] == 0.94
    assert "RULE_001" in data["matched_rules"]
