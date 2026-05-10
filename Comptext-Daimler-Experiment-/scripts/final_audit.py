import requests
import json
import time

API_URL = "http://localhost:8000"

BENCHMARK_SUITE = [
    {
        "label": "CRITICAL: XENTRY Brake Failure (P1)",
        "text": """
        XENTRY Diagnosis Report - 2026-05-09
        VIN: WDB906232N3123456
        System: Brake Control
        Fault: P0300, P0500 Speed Sensor Correlation
        Observation: ABS light flashing. Emergency brake force reduced.
        Urgency: Immediate production stop required.
        """
    },
    {
        "label": "URGENT: MO360 Line Bottleneck (P2)",
        "text": """
        MO360 Industrial Insight - Shift B
        Line: Assembly 4
        Metric: Uptime 82% (Target 95%)
        Deviation: Robot arm KR-500 showing thermal jitter.
        Recommendation: Recalibration within 24 hours to avoid downtime.
        """
    },
    {
        "label": "ROUTINE: SAP Logistics Sync (P3)",
        "text": """
        SAP-MM Automated Update
        PO: 4500987654
        Material: OIL-FILTER-MB
        Quantity: 200 units
        Status: Inventory received and verified by scanner S-12.
        Next Step: Update warehouse ledger.
        """
    }
]

def run_final_audit():
    print("="*75)
    print("   COMPTEXT V6-TURBO x CLAUDE 3.5 SONNET : FINAL INDUSTRIAL AUDIT")
    print("="*75)
    print(f"{'Scenario':<35} | {'Reduc':<7} | {'Latency':<10} | {'Status'}")
    print("-" * 75)

    results = []

    for case in BENCHMARK_SUITE:
        t0 = time.perf_counter()
        try:
            resp = requests.post(f"{API_URL}/analyze", json={"text": case["text"], "quelle": "Audit-V6"}).json()
            latency = (time.perf_counter() - t0) * 1000
            
            savings = resp.get("metrics", {}).get("savings", 0)
            prio = resp.get("prioritaet", "N/A")
            
            # Simple integrity check
            status = "🟢 VALID" if prio != "P3_ROUTINE" or "SAP" in case["label"] else "🟡 CHECK"
            
            print(f"{case['label']:<35} | {savings:>6.1f}% | {latency:>8.0f}ms | {status}")
            
            results.append({
                "label": case["label"],
                "summary": resp.get("zusammenfassung", ""),
                "prio": prio,
                "latency": latency,
                "savings": savings
            })
        except Exception as e:
            print(f"{case['label']:<35} | ERROR: {e}")

    print("-" * 75)
    avg_latency = sum(r["latency"] for r in results) / len(results) if results else 0
    avg_savings = sum(r["savings"] for r in results) / len(results) if results else 0
    
    print(f"OVERALL PERFORMANCE: Avg Latency {avg_latency:.0f}ms | Avg Savings {avg_savings:.1f}%")
    print("="*75)
    
    # Detailed Analysis for the P1 Case
    if results:
        p1 = results[0]
        print(f"\n[DEEP DIVE: {p1['label']}]")
        print(f"AI ANALYSIS: {p1['summary']}")
        print(f"AI PRIORITY: {p1['prio']}")

if __name__ == "__main__":
    run_final_audit()
