import time
import requests
import json
import os

API_URL = "http://localhost:8000"

# Simulate a MASSIVE 24h XENTRY log with hundreds of repetitive entries
HEAVY_LOG = """
[SYSTEM START] Daimler Buses Telemetry - Fleet ID: 5000-X
TIMESTAMP | MODULE | STATUS | DATA
""" + "\n".join([
    f"2026-05-09 {h:02d}:{m:02d}:00 | BRK-CTRL | OK | Volt={12.0 + (m/100):.1f}V Temp=45.2C"
    for h in range(0, 24) for m in range(0, 60, 5)
]) + """
CRITICAL EVENT:
2026-05-09 18:45:22 - P0300 Random Misfire detected in Cylinder 1.
2026-05-09 18:45:23 - P0500 Speed Sensor mismatch.
2026-05-09 18:45:24 - Status: P1 Escalation Triggered.
2026-05-09 18:45:25 - VIN: WDB906232N3123456
2026-05-09 18:45:26 - Technician: PERS_99887766
[SYSTEM END]
"""

def run_industrial_stress_test():
    print("="*80)
    print("      REAL SCENARIO BENCHMARK: 24H FLEET TELEMETRY (INDUSTRIAL LOAD)")
    print("="*80)
    
    # Payload Stats
    orig_chars = len(HEAVY_LOG)
    orig_tokens = orig_chars // 4
    
    print(f"[*] Input Data Size:  {orig_chars} chars (~{orig_tokens} tokens)")
    print(f"[*] Target Model:     Claude 3.5 Sonnet (Native CLI)")
    print(f"[*] Compression:      V6-Turbo Extreme (>90% Mode)")
    print("-" * 80)

    t0 = time.perf_counter()
    try:
        # 1. Standalone Compression Performance
        print(f"[*] Step 1: Executing Extreme KVTC Mining...")
        comp_resp = requests.post(f"{API_URL}/compress", json={"text": HEAVY_LOG}).json()
        comp_tokens = comp_resp["compressed_tokens"]
        savings = comp_resp["token_reduction_pct"]
        kvtc_latency = comp_resp["latency_ms"]
        
        print(f"    >> Frame Size:    {len(comp_resp['frame'])} chars")
        print(f"    >> Tokens:        {comp_tokens}")
        print(f"    >> Reduction:     {savings}%")
        print(f"    >> Mining Time:   {kvtc_latency:.2f}ms")
        print("-" * 80)

        # 2. Full End-to-End Analysis (including Claude reasoning)
        print(f"[*] Step 2: Dispatching Bottleneck to Claude CLI...")
        full_resp = requests.post(f"{API_URL}/analyze", json={"text": HEAVY_LOG, "quelle": "Fleet-Stress-Test"}).json()
        total_latency = (time.perf_counter() - t0) * 1000
        
        print(f"\n[FINAL PROJECTED RESULTS]")
        print(f"AI Decision:      {full_resp.get('prioritaet', 'N/A')}")
        print(f"AI Reasoning:     {full_resp.get('zusammenfassung', 'N/A')[:150]}...")
        print(f"E2E Latency:      {total_latency:.0f}ms")
        
        # 3. ROI Calculation (Projected)
        # Avg cost per 1M tokens = $3.00 (Input)
        cost_orig = (orig_tokens / 1_000_000) * 3.00
        cost_comp = (comp_tokens / 1_000_000) * 3.00
        annual_savings = (cost_orig - cost_comp) * 365 * 5000 # Fleet of 5k buses
        
        print("-" * 80)
        print(f"ANNUAL FLEET ROI: ${annual_savings:,.2f} USD SAVED / YEAR")
        print("="*80)

    except Exception as e:
        print(f"\n[ERROR] Stress test failed. Is the API running?\nDetail: {e}")

if __name__ == "__main__":
    run_industrial_stress_test()
