"""
Runner – Executes the Batch Evolution Loop.
"""

import os
import yaml
import json
from validation.batch_evolution_loop.orchestrator import Orchestrator

def mock_sandbox_eval(patch: str) -> dict:
    """
    Simulates /validation/autoresearch_sandbox/run_experiment
    Deterministically derived from the patch string.
    """
    # Deterministic pseudo-randomness based on patch content
    val = sum(ord(c) for c in patch)
    return {
        "correctness": round((val % 100) / 100.0, 2),
        "performance": round((val % 80) / 100.0, 2),
        "regression_risk": round((val % 20) / 100.0, 2)
    }

def main():
    # Load config
    config_path = "validation/batch_evolution_loop/config.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    else:
        config = {
            "batch_size": 10,
            "seed": 42,
            "scoring_weights": {"correctness": 0.55, "performance": 0.30, "regression_risk": 0.15}
        }

    print(f"[*] Initializing Batch Evolution Loop (Seed: {config.get('seed')})")
    
    orchestrator = Orchestrator(config)
    
    base_state = {"id": "comptext_v6_base", "version": "6.0.0"}
    
    print(f"[*] Running batch of size {config.get('batch_size')}...")
    
    # In a real integration, this would point to the actual sandbox runner
    ranked_results = orchestrator.run_batch(base_state, mock_sandbox_eval)
    
    print("\n" + "="*50)
    print("RANKED CANDIDATES (Top 3)")
    print("="*50)
    
    for i, res in enumerate(ranked_results[:3]):
        print(f"{i+1}. {res['id']} | Score: {res['score']} | Correctness: {res['correctness']}")

    print("\n[*] Batch execution complete. History updated in memory.")
    
    # Final output for stdout as required
    print(json.dumps(ranked_results[:3], indent=2))

if __name__ == "__main__":
    main()
