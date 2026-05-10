"""
Scorer – Multi-metric evaluation for candidate patches.
"""

from typing import Dict

class Scorer:
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            "correctness": 0.55,
            "performance": 0.30,
            "regression_risk": 0.15
        }

    def score(self, evaluation: Dict[str, float]) -> Dict[str, float]:
        """
        Implements multi-metric scoring function:
        score = 0.55 * correctness + 0.30 * performance - 0.15 * regression_risk
        """
        correctness = evaluation.get("correctness", 0.0)
        performance = evaluation.get("performance", 0.0)
        risk = evaluation.get("regression_risk", 0.0)

        total_score = (
            self.weights["correctness"] * correctness +
            self.weights["performance"] * performance -
            self.weights["regression_risk"] * risk
        )

        return {
            "score": round(float(total_score), 4),
            "correctness": float(correctness),
            "performance": float(performance),
            "regression_risk": float(risk)
        }
