"""
Benchmark Suite V1 Runner – Formal Evaluation Set.
Measures Token Reduction, Latency, and Semantic Alignment for V6-Turbo Extreme.
"""

import requests
import json
import time
import os
import sys

API_URL = "http://localhost:8000"
SET_PATH = "validation/benchmark_suite_v1/evaluation_set.json"

def print_header():
    print("\n" + "="*95)
    print("      COMPTEXT V6 PLATFORM – BENCHMARK SUITE V1 (REAL EVALUATION SET)")
    print("="*95)
    print(f"{'ID':<7} | {'Scenario':<32} | {'Reduc':<7} | {'Lat':<8} | {'Prio (Exp/AI)':<20} | {'Status'}")
    print("-" * 95)

def run_suite():
    if not os.path.exists(SET_PATH):
        print(f"Error: Evaluation set not found at {SET_PATH}")
        return

    with open(SET_PATH, "r") as f:
        evaluation_set = json.load(f)

    print_header()
    
    results = []
    total_savings = 0
    total_latency = 0
    matches = 0

    for case in evaluation_set:
        try:
            t0 = time.perf_counter()
            resp = requests.post(f"{API_URL}/analyze", json={"text": case["text"], "quelle": "BS-V1"}).json()
            latency = (time.perf_counter() - t0) * 1000
            
            # Metrics
            savings = resp.get("token_einsparung_pct", 0)
            ai_prio = resp.get("prioritaet", "N/A")
            exp_prio = case["expected_prio"]
            
            # Semantic Alignment Check
            is_match = ai_prio.split("_")[0] == exp_prio.split("_")[0] # Compare base P1/P2/P3
            status = "🟢 PASS" if is_match else "🔴 FAIL"
            
            if is_match: matches += 1
            total_savings += savings
            total_latency += latency
            
            print(f"{case['id']:<7} | {case['label'][:32]:<32} | {savings:>6.1f}% | {latency:>6.0f}ms | {exp_prio[:2]} / {ai_prio[:2]:<13} | {status}")
            
            results.append({
                "id": case["id"],
                "savings": savings,
                "latency": latency,
                "alignment": is_match,
                "ai_summary": resp.get("zusammenfassung", "")
            })
        except Exception as e:
            print(f"{case['id']:<7} | {case['label'][:32]:<32} | ERROR: {e}")

    # Summary
    print("-" * 95)
    count = len(results)
    if count > 0:
        avg_savings = total_savings / count
        avg_latency = total_latency / count
        accuracy = (matches / count) * 100
        
        print(f"SUMMARY: Avg Savings: {avg_savings:.1f}% | Avg Latency: {avg_latency:.0f}ms | Semantic Accuracy: {accuracy:.1f}%")
    
    print("="*95)
    
    # Detailed output for specific Compound case
    if count >= 5:
        print(f"\n[EVALUATION DEEP-DIVE: {results[4]['id']}]")
        print(f"AI SUMMARY: {results[4]['ai_summary']}")

if __name__ == "__main__":
    run_suite()
