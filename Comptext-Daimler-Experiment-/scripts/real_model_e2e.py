import requests
import json
import time

API_URL = "http://localhost:8000"

# Complex XENTRY Case
DIAGNOSTIC_DATA = """
Wartungsprotokoll MB-TRUCK-2026-05
Fahrzeug-FIN: WDB906232N3123456
Fehler: P0300 Zündaussetzer Zylinder 1-4
Symptom: Motor ruckelt bei Volllast.
Status: Prio 1 Eskalation erforderlich.
Techniker: P12345
"""

def test_real_model_inference():
    print("="*60)
    print("   E2E VALIDATION: COMPTEXT V6-TURBO x CLAUDE CLI (Terminal)")
    print("="*60)
    
    payload = {"text": DIAGNOSTIC_DATA, "quelle": "E2E-Validation"}
    
    t0 = time.perf_counter()
    try:
        # Full Analyze Pipeline (Intake -> Triage -> Analysis)
        resp = requests.post(f"{API_URL}/analyze", json=payload).json()
        latency = (time.perf_counter() - t0) * 1000
        
        print(f"[*] Response Status: {resp.get('status', 'N/A')}")
        print(f"[*] Latency:         {latency:.2f}ms")
        print(f"[*] AI Summary:      {resp.get('zusammenfassung', 'No summary')}")
        print(f"[*] AI Priority:     {resp.get('prioritaet', 'Unknown')}")
        print(f"[*] AI Action:       {', '.join(resp.get('massnahmen', []))}")
        print(f"[*] Token Savings:   {resp.get('metrics', {}).get('savings', 0)}%")
        
        # Verify correctness
        if "P0300" in str(resp) and "P1" in resp.get('prioritaet', ''):
            print("\n[SUCCESS] Claude CLI correctly interpreted the compressed V6-Turbo frame.")
        else:
            print("\n[WARNING] Potential semantic loss or model misinterpretation.")
            print(f"[DEBUG] Raw Response: {json.dumps(resp, indent=2)}")

    except Exception as e:
        print(f"[ERROR] Connection to API or Model failed: {e}")

if __name__ == "__main__":
    test_real_model_inference()
