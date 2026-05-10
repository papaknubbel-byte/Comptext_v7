from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class DecisionStep:
    iteration: int
    route: str
    confidence: float
    reason: str
    action: str
    observation: str


class DecisionTrace:
    def __init__(self) -> None:
        self._steps: list[DecisionStep] = []

    def add(self, step: DecisionStep) -> None:
        self._steps.append(step)

    def as_dict(self) -> dict[str, Any]:
        explanations = [
            f"Step {s.iteration}: route={s.route}, confidence={s.confidence:.2f}, action={s.action}"
            for s in self._steps
        ]
        return {"steps": [asdict(s) for s in self._steps], "explanations": explanations}
