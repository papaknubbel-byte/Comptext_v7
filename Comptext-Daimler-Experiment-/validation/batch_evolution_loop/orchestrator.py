"""
Orchestrator – Core entry point for batch execution.
"""

from typing import List, Dict
import random
from .generator import Generator
from .scorer import Scorer
from .memory import Memory

class Orchestrator:
    def __init__(self, config: Dict):
        self.config = config
        self.seed = config.get("seed", 42)
        self.batch_size = config.get("batch_size", 10)
        self.generator = Generator(seed=self.seed)
        self.scorer = Scorer(weights=config.get("scoring_weights"))
        self.memory = Memory()

    def run_batch(self, base_state: Dict, sandbox_callback) -> List[Dict]:
        """
        Controls full lifecycle:
        generate -> evaluate (via sandbox) -> score -> rank -> store
        """
        # 1. Generate
        candidates = self.generator.generate(base_state, count=self.batch_size)
        
        results = []
        
        # 2. Evaluate
        for cand in candidates:
            # Deterministic evaluation via sandbox
            eval_metrics = sandbox_callback(cand["patch"])
            
            # 3. Score
            score_data = self.scorer.score(eval_metrics)
            
            result = {
                **cand,
                **score_data
            }
            results.append(result)
            
            # 4. Store
            self.memory.save_result(result)
            
        # 5. Rank
        ranked_results = sorted(results, key=lambda x: x["score"], reverse=True)
        
        return ranked_results
