import time
import requests
import json

API_URL = "http://localhost:8000"

BENCHMARK_CASES = [
    {
        "label": "XENTRY Diagnostic Log",
        "text": """
        2026-05-09 14:30:21 - Initializing XENTRY Diagnosis
        Vehicle VIN: WDB906232N3123456
        Odometer: 125430 km
        System: Brake Control Unit (BCU)
        Check Status: Voltage 12.4V, Temp 45C
        Current Fault: P0300 Random Misfire Detected
        Odometer at Fault: 125428 km
        Counter: 12
        Result: Analysis completed.
        """
    },
    {
        "label": "MO360 Shift Report",
        "text": """
        MO360 Production Line A - Shift Report
        Date: 2026-05-08
        Shift: Morning
        Unit ID: SAP-9928341
        Production Status: OK
        Output: 450 units
        Downtime: 5 mins (maintenance verified)
        Notes: Line speed stable at 45.2 m/min.
        """
    },
    {
        "label": "SAP Supply Chain Update",
        "text": """
        SAP-MM Purchase Order 4500123456
        Vendor: Parts-Logistics GmbH
        Material: BRAKE-PAD-V6
        Quantity: 500
        Status: Shipped
        ETA: 2026-05-12
        Verification: QR-Code check OK.
        """
    }
]

def run_comprehensive_benchmark():
    print("="*60)
    print("   COMPTEXT V6-TURBO ULTIMATE+ : TOKEN REDUCTION REPORT")
    print("="*60)
    print(f"{'Scenario':<25} | {'Orig':<5} | {'Comp':<5} | {'Reduction':<10}")
    print("-"*60)

    total_orig = 0
    total_comp = 0

    for case in BENCHMARK_CASES:
        try:
            resp = requests.post(f"{API_URL}/compress", json={"text": case["text"]}).json()
            orig = resp["original_tokens"]
            comp = resp["compressed_tokens"]
            red = resp["token_reduction_pct"]
            
            total_orig += orig
            total_comp += comp
            
            print(f"{case['label']:<25} | {orig:<5} | {comp:<5} | {red:>8.1f}%")
            print(f"  > Frame: {resp['frame'][:100]}...")
        except Exception as e:
            print(f"[ERROR] {case['label']}: {e}")

    avg_reduction = (1 - total_comp / total_orig) * 100 if total_orig > 0 else 0
    
    print("-"*60)
    print(f"{'TOTAL / AVERAGE':<25} | {total_orig:<5} | {total_comp:<5} | {avg_reduction:>8.1f}%")
    print("="*60)

if __name__ == "__main__":
    run_comprehensive_benchmark()
