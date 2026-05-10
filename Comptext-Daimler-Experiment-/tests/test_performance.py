import time
import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_copilot_preview_performance():
    """
    Validates that the copilot preview endpoint returns within acceptable time limits (mock mode).
    """
    payload = {
        "text": "P0300 Zündaussetzer erkannt. Sofortige Wartung erforderlich.",
        "quelle": "PerfTest"
    }
    
    t0 = time.perf_counter()
    response = client.post("/v1/copilot/preview", json=payload)
    latency = (time.perf_counter() - t0) * 1000
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "copilot_attachment" in data
    assert "explanation" in data["copilot_attachment"]
    
    # In mock mode, this should be very fast
    assert latency < 500 # ms

def test_batch_analyze_concurrency():
    """
    Simple check for batch analyze with multiple items.
    """
    payload = {
        "documents": [
            {"text": f"Doc {i}: Fehlercode P0300", "quelle": "PerfTest"} 
            for i in range(5)
        ]
    }
    
    response = client.post("/batch/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert data["succeeded"] == 5
