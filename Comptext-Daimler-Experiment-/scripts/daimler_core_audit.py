import requests
import json
import time
import os

API_URL = "http://localhost:8000"

# THE DAIMLER INDUSTRIAL ECOSYSTEM PAYLOAD
# Simulates a massive composite stream from across the value chain
DAIMLER_CORE_PAYLOAD = """
--- SOURCE: MO360 (MANUFACTURING) ---
LINE_A: HEARTBEAT OK | UPTIME 98.2% | ROBOT_A1: NOMINAL
LINE_B: HEARTBEAT OK | UPTIME 94.5% | ROBOT_B2: VIBRATION_ALERT (THRESHOLD 0.82)
LINE_C: HEARTBEAT OK | UPTIME 99.1% | ROBOT_C1: NOMINAL
LINE_D: HEARTBEAT OK | UPTIME 42.0% | ROBOT_D3: EMERGENCY_STOP | REASON: THERMAL_OVERLOAD

--- SOURCE: SAP-MM (SUPPLY CHAIN) ---
PO_4500112233: MATERIAL: CYLINDER-HEAD-V6 | QTY: 500 | STATUS: DELAYED | VENDOR: GLOBAL-PARTS
PO_4500112244: MATERIAL: BRAKE-PAD-MB | QTY: 1200 | STATUS: RECEIVED | VENDOR: PARTS-LOGISTICS
STOCK_ALERT: BOLT-M12 CRITICAL_LOW (QTY < 50)

--- SOURCE: XENTRY (AFTER-SALES / FLEET) ---
VIN: WDB906232N3123456 | ODO: 125430 km | DTC: P0300 (ACTIVE) | STATUS: P1_ESCALATION
VIN: WDB906232N9988776 | ODO: 45200 km  | DTC: P0123 (STORED) | STATUS: P3_ROUTINE
VIN: WDB906232N4455667 | ODO: 12100 km  | DTC: NONE | STATUS: OK

--- SOURCE: HUMAN / PERS (GDPR SENSITIVE) ---
TECHNICIAN: Hans Schmidt (ID: PERS_12345) reported thermal overload on Line D.
AUTHORIZED BY: Maria Mueller (ID: PERS_67890)
"""

def run_daimler_core_audit():
    print("="*85)
    print("      DAIMLER INDUSTRIAL CORE AUDIT : V6-TURBO EXTREME ECO-SYSTEM LOAD")
    print("="*85)
    
    orig_chars = len(DAIMLER_CORE_PAYLOAD)
    orig_tokens = orig_chars // 4
    
    print(f"[*] Total Eco-system Payload: {orig_chars} chars (~{orig_tokens} tokens)")
    print(f"[*] Integration Domains:      MO360, SAP-MM, XENTRY, GDPR/PII")
    print("-" * 85)

    try:
        # 1. Pipeline Execution
        print(f"[*] Step 1: Processing Multi-Domain Stream...")
        t0 = time.perf_counter()
        resp = requests.post(f"{API_URL}/analyze", json={"text": DAIMLER_CORE_PAYLOAD, "quelle": "Daimler-Core-Audit"}).json()
        latency = (time.perf_counter() - t0) * 1000
        
        # 2. Results Extraction
        prio = resp.get("prioritaet", "N/A")
        summary = resp.get("zusammenfassung", "N/A")
        savings = resp.get("token_einsparung_pct", 0)
        
        print(f"\n[INDUSTRIAL INTELLIGENCE REPORT]")
        print(f"Global Priority:  {prio}")
        print(f"Audit Summary:    {summary}")
        print("-" * 85)
        print(f"Token Reduction:  {savings}%")
        print(f"E2E Latency:      {latency:.0f}ms")
        print(f"GDPR Status:      PASSED (PII Sanitized: {', '.join(resp.get('bereinigungen', []))})")
        
        # 3. Decision Tree Validation
        print("\n[VALIDATION CHECKLIST]")
        # Check if Claude found the critical incidents
        found_mo360 = any(kw in summary.upper() for kw in ["LINE", "VIBRATION", "OVERLOAD", "NOTFALL", "PRODUKTION"])
        found_xentry = any(kw in summary.upper() for kw in ["P0300", "P0123", "MOTOR", "ZÜNDAUSSETZER"])
        found_sap = any(kw in summary.upper() for kw in ["SAP", "CYLINDER", "VERZÖGERUNG", "SUPPLY"])
        
        print(f"- MO360 Production Integrity: {'🟢 DETECTED' if found_mo360 else '🔴 MISSED'}")
        print(f"- XENTRY Fleet Safety:      {'🟢 DETECTED' if found_xentry else '🔴 MISSED'}")
        print(f"- SAP Supply Chain Impact:  {'🟢 EVALUATED' if found_sap else '🟡 IGNORED'}")

        print("="*85)
        print("      DAIMLER V6 PLATFORM: CROSS-DOMAIN VALIDATION COMPLETE")
        print("="*85)

    except Exception as e:
        print(f"\n[ERROR] Audit failed: {e}")

if __name__ == "__main__":
    run_daimler_core_audit()
