"""
Generator – Produces candidate patches or mutations.
"""

import random
from typing import List, Dict

class Generator:
    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)

    def generate(self, base_state: Dict, count: int = 10) -> List[Dict]:
        """
        Produces N candidate patches.
        Simulates deterministic mutation of a base state.
        """
        candidates = []
        for i in range(count):
            candidate = {
                "id": f"cand_{i}_{self.seed}",
                "base": base_state.get("id", "base"),
                "patch": f"mutation_v{i}",
                "metadata": {
                    "mutation_type": random.choice(["perf_opt", "logic_fix", "refactor"]),
                    "impact_estimate": random.uniform(0.1, 0.9)
                }
            }
            candidates.append(candidate)
        return candidates
