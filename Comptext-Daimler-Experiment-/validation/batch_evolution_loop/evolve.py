"""
Evolve – Automates multi-generation evolution cycles.
"""

import os
import yaml
import json
from validation.batch_evolution_loop.orchestrator import Orchestrator
from validation.batch_evolution_loop.memory import Memory

def mock_sandbox_eval(patch: str) -> dict:
    """
    Deterministic evaluation derived from patch + base strings.
    Simulates improvement over generations.
    """
    # Deterministic but generation-aware pseudo-randomness
    val = sum(ord(c) for c in patch)
    return {
        "correctness": min(1.0, round((val % 100) / 100.0 + 0.05, 2)),
        "performance": min(1.0, round((val % 80) / 100.0 + 0.1, 2)),
        "regression_risk": max(0.0, round((val % 20) / 100.0 - 0.02, 2))
    }

def main(generations: int = 3):
    # Load config
    config_path = "validation/batch_evolution_loop/config.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    else:
        config = {"batch_size": 10, "seed": 42}

    memory = Memory()
    
    # Check if we have a previous best to start from
    current_best = memory.load_best()
    if not current_best:
        print("[*] No existing history found. Starting from base system state.")
        base_state = {"id": "comptext_v6_base", "version": "6.0.0", "score": 0.0}
    else:
        print(f"[*] Resuming from previous best: {current_best['id']} (Score: {current_best['score']})")
        base_state = current_best

    for gen in range(1, generations + 1):
        print(f"\n" + "="*60)
        print(f" GENERATION {gen}")
        print("="*60)
        
        # Shift seed for each generation to explore different mutation spaces
        config["seed"] = config.get("seed", 42) + gen
        orchestrator = Orchestrator(config)
        
        print(f"[*] Running evolution batch (Size: {config['batch_size']})...")
        ranked_results = orchestrator.run_batch(base_state, mock_sandbox_eval)
        
        top_cand = ranked_results[0]
        improvement = top_cand["score"] - base_state.get("score", 0.0)
        
        print(f"[*] Best Candidate: {top_cand['id']}")
        print(f"[*] Score: {top_cand['score']} (Change: {improvement:+.4f})")
        print(f"[*] Correctness: {top_cand['correctness']} | Performance: {top_cand['performance']}")
        
        # Update base for next generation
        base_state = top_cand

    print("\n" + "="*60)
    print(" EVOLUTIONARY SPRINT COMPLETE")
    print("="*60)
    final_best = memory.load_best()
    print(f"Final Champion: {final_best['id']} | Score: {final_best['score']}")

if __name__ == "__main__":
    main()
