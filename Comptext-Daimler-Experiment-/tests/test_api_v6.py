import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_copilot_preview_endpoint():
    """
    Validates the new V1 Copilot Preview endpoint.
    """
    payload = {
        "text": "P0300 Zündaussetzer. Kritisch.",
        "quelle": "IntegrationTest"
    }
    response = client.post("/v1/copilot/preview", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "copilot_attachment" in data
    assert "diagnostics_uri" in data
    assert data["diagnostics_uri"].startswith("comptext://")

def test_compress_endpoint():
    """
    Tests the standalone KVTC compression endpoint.
    """
    payload = {"text": "Wartungsprotokoll 123. Kilometerstand 50000. Bremse OK."}
    response = client.post("/compress", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "frame" in data
    assert data["original_tokens"] > data["compressed_tokens"]

def test_triage_endpoint():
    """
    Tests the priority triage endpoint.
    """
    payload = {"text": "BREMSENAUSFALL kritisch!", "doc_type": "FREITEXT"}
    response = client.post("/triage", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prioritaet"] == "P1_KRITISCH"
    assert "ausgeloeste_regeln" in data

def test_copilot_preview_error_handling():
    """
    Tests error handling in the copilot endpoint.
    """
    # Empty text triggers Pydantic validation error (min_length=1)
    # api.py returns status_code=400 for validation errors
    payload = {"text": "", "quelle": "Test"}
    response = client.post("/v1/copilot/preview", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
