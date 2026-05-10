import time
import requests
import sys
import os

# Configuration
API_URL = "http://localhost:8000"
DASHBOARD_URL = "http://localhost:5173"

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*80)
    print("      COMPTEXT V6 PLATFORM – INDUSTRIAL BENCHMARK MONITOR")
    print("="*80)
    print(f"Target API: {API_URL}")
    print(f"Showcase:   {DASHBOARD_URL}")
    print("-"*80)

def run_benchmarks():
    try:
        # Check Health
        health = requests.get(f"{API_URL}/health").json()
        
        # Run Standard Benchmark Endpoint
        print(f"[*] Starting standard industrial benchmark...")
        bench_start = time.time()
        results = requests.get(f"{API_URL}/benchmark").json()
        duration = time.time() - bench_start
        
        print_header()
        print(f"Health Status: {health.get('status', 'OFFLINE')} | Cache Size: {health.get('cache_size', 0)}")
        print("-"*80)
        print(f"{'Scenario':<25} | {'Orig Tok':<10} | {'Comp Tok':<10} | {'Savings':<10}")
        print("-"*80)
        
        for res in results.get("results", []):
            label = res.get("label", "Unknown")
            orig = res.get("original_tokens", 0)
            comp = res.get("compressed_tokens", 0)
            sav = res.get("reduction_pct", 0.0)
            print(f"{label:<25} | {orig:<10} | {comp:<10} | {sav:>8.2f}%")
            
        print("-"*80)
        print(f"Total Benchmark Duration: {duration:.3f}s")
        print("-"*80)
        
        # Real-time Metrics Simulation
        print("\n[*] Monitoring Live Throughput (Press Ctrl+C to stop)...")
        while True:
            # Simulate a live diagnostic ingest
            t0 = time.perf_counter()
            requests.post(f"{API_URL}/v1/optimize/xentry", json={"log_lines": 50})
            latency = (time.perf_counter() - t0) * 1000
            
            # Fetch latest stats
            stats = requests.get(f"{API_URL}/health").json()
            
            sys.stdout.write(f"\r >> Latency: {latency:7.2f}ms | Hit Rate: {stats.get('cache_hit_rate', 0.0):.1f}% | Processed: {stats.get('cache_size', 0)} docs")
            sys.stdout.flush()
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n[*] Benchmark Monitoring stopped by user.")
    except Exception as e:
        print(f"\n[ERROR] Connection to API failed. Ensure 'python api.py' is running.")
        print(f"Detail: {e}")

if __name__ == "__main__":
    run_benchmarks()
