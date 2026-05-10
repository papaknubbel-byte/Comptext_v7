"""
Stress Test Script for CompText V6 Platform.
Sends concurrent requests to /batch/analyze and /v1/copilot/preview.
"""

import asyncio
import httpx
import time
import json

BASE_URL = "http://localhost:8000"

async def test_batch_analyze(client, i):
    payload = {
        "documents": [
            {"text": f"Stress Test Doc {i}.1: P0300 detected.", "quelle": "StressTest"},
            {"text": f"Stress Test Doc {i}.2: Routine maintenance.", "quelle": "StressTest"}
        ]
    }
    start = time.perf_counter()
    try:
        resp = await client.post(f"{BASE_URL}/batch/analyze", json=payload)
        latency = (time.perf_counter() - start) * 1000
        return resp.status_code, latency
    except Exception as e:
        return str(e), 0

async def test_copilot_preview(client, i):
    payload = {
        "text": f"Stress Test Copilot {i}: Critical engine failure.",
        "quelle": "StressTest"
    }
    start = time.perf_counter()
    try:
        resp = await client.post(f"{BASE_URL}/v1/copilot/preview", json=payload)
        latency = (time.perf_counter() - start) * 1000
        return resp.status_code, latency
    except Exception as e:
        return str(e), 0

async def main(iterations=50, concurrency=10):
    print(f"Starting Stress Test: {iterations} iterations, concurrency={concurrency}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Check health first
        try:
            await client.get(f"{BASE_URL}/health")
        except:
            print(f"ERROR: Could not connect to {BASE_URL}. Is the server running?")
            return

        tasks = []
        for i in range(iterations):
            tasks.append(test_batch_analyze(client, i))
            tasks.append(test_copilot_preview(client, i))
            
            if len(tasks) >= concurrency:
                results = await asyncio.gather(*tasks)
                tasks = []
                # Simple progress
                print(".", end="", flush=True)

        if tasks:
            await asyncio.gather(*tasks)
            
    print("\nStress Test Completed.")

if __name__ == "__main__":
    asyncio.run(main())
