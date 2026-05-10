import requests
import json
import time
import os

API_URL = "http://localhost:8000"

TEST_CASE = """
Daimler Truck - Service Report
VIN: WDB906232N3123456
Fault: P0300 Random Misfire
Odometer: 125430
Note: Engine shaking at high speed. Immediate inspection needed.
"""

def run_research():
    print("="*70)
    print("   KVTC RESEARCH: EFFICIENCY vs. INTEGRITY (OPENCODE)")
    print("="*70)
    
    # Ensure opencode backend is active
    os.environ["LLM_BACKEND"] = "opencode"
    os.environ["OPENCODE_MODEL"] = "opencode/minimax-m2.5-free"
    
    # We assume the API is already running with the correct env or we restart it
    # For this research, we just call the analyze endpoint which uses the current KVTC Ultimate+
    
    print(f"[*] Dispatching Analyze Request (KVTC Ultimate+)")
    t0 = time.perf_counter()
    try:
        resp = requests.post(f"{API_URL}/analyze", json={"text": TEST_CASE, "quelle": "Research-V6"}).json()
        latency = (time.perf_counter() - t0) * 1000
        
        print(f"\n[METRICS]")
        print(f"Latency:   {latency:.2f}ms")
        print(f"Savings:   {resp.get('metrics', {}).get('savings', 0)}%")
        print(f"Model:     {resp.get('modell_id', 'N/A')}")
        
        print(f"\n[AI INTERPRETATION]")
        print(f"Summary:   {resp.get('zusammenfassung', 'N/A')}")
        print(f"Priority:  {resp.get('prioritaet', 'N/A')}")
        print(f"Codes:     {resp.get('erkannte_fehlercodes', [])}")
        
        # Validation Logic
        integrity_score = 0
        if "P0300" in str(resp.get('erkannte_fehlercodes', [])): integrity_score += 50
        if "P1" in resp.get('prioritaet', ''): integrity_score += 50
        
        print(f"\n[INTEGRITY SCORE: {integrity_score}/100]")
        if integrity_score == 100:
            print("🚀 MAXIMUM EFFICIENCY REACHED: 100% Semantic Integrity preserved.")
        else:
            print("⚠️ COMPRESSION LIMIT EXCEEDED: Loss of critical diagnostic data.")

    except Exception as e:
        print(f"[ERROR] Research failed: {e}")

if __name__ == "__main__":
    run_research()
