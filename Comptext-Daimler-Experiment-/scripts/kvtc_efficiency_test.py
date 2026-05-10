import time
import requests
import sys

API_URL = "http://localhost:8000"

# Sample XENTRY Diagnostic Log with high redundancy
SAMPLE_LOG = """
SOP Start 2026-05-09 10:00:00
Vehicle VIN: WDB906232N3123456
System: Brake Control Unit
Odometer: 125430 km

Log Event 001: 2026-05-09 08:30:00 - Status OK
Log Event 002: 2026-05-09 08:31:00 - Voltage 12.4V
Log Event 003: 2026-05-09 08:32:00 - Temp 45C
Log Event 004: 2026-05-09 08:33:00 - Status OK
Log Event 005: 2026-05-09 08:34:00 - Voltage 12.3V
Log Event 006: 2026-05-09 08:35:00 - Temp 46C
Log Event 007: 2026-05-09 08:36:00 - Status OK
Log Event 008: 2026-05-09 08:37:00 - Voltage 12.4V
Log Event 009: 2026-05-09 08:38:00 - Temp 45C
Log Event 010: 2026-05-09 08:39:00 - Status OK

Current Fault: P0300 - Random Misfire Detected
Odometer at Fault: 125428 km
Counter: 12
"""

def test_efficiency():
    print(f"[*] Running KVTC Efficiency Benchmark...")
    
    payload = {"text": SAMPLE_LOG}
    try:
        resp = requests.post(f"{API_URL}/compress", json=payload).json()
        orig = resp["original_tokens"]
        comp = resp["compressed_tokens"]
        red = resp["token_reduction_pct"]
        
        print(f"Original Tokens:   {orig}")
        print(f"Compressed Tokens: {comp}")
        print(f"Reduction:         {red}%")
        print(f"Full Frame:        {resp['frame']}")
        
        return red
    except Exception as e:
        print(f"Error: {e}")
        return 0.0

if __name__ == "__main__":
    test_efficiency()
