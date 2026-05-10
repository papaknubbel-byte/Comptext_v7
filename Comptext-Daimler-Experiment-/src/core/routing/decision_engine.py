from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RoutingWeights:
    relevance: float = 0.45
    confidence: float = 0.35
    token_cost: float = 0.15
    cache_hit: float = 0.05


class DecisionEngine:
    def __init__(self, weights: RoutingWeights | None = None, deterministic: bool = False, fallback_route: str = "llm") -> None:
        self.weights = weights or RoutingWeights()
        self.deterministic = deterministic
        self.fallback_route = fallback_route

    def decide(self, compressed_state: dict[str, Any] | str, intent: str, context_metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        ctx = context_metadata or {}
        if not intent:
            return self._fallback("missing_intent", 0.0)

        relevance = self._score_relevance(compressed_state, intent)
        confidence = float(ctx.get("confidence", 0.5))
        token_cost = float(ctx.get("token_cost", self._estimate_cost(compressed_state)))
        cache_hit = 1.0 if ctx.get("cache_hit") else 0.0

        score = (
            self.weights.relevance * relevance
            + self.weights.confidence * confidence
            - self.weights.token_cost * token_cost
            + self.weights.cache_hit * cache_hit
        )
        route = self._route_from_score(score, cache_hit, ctx)
        return {
            "route": route,
            "confidence": round(max(0.0, min(1.0, score)), 4),
            "reason": f"score={score:.4f}, rel={relevance:.3f}, conf={confidence:.3f}, token_cost={token_cost:.3f}, cache_hit={cache_hit}",
            "cost_estimate": round(token_cost, 4),
        }

    def _score_relevance(self, compressed_state: dict[str, Any] | str, intent: str) -> float:
        if isinstance(compressed_state, dict):
            text = " ".join(str(v) for v in compressed_state.values())
        else:
            text = compressed_state
        intent_terms = {t.lower() for t in intent.split() if t}
        if not intent_terms:
            return 0.0
        text_terms = {t.lower() for t in str(text).split()}
        overlap = len(intent_terms & text_terms)
        base = overlap / max(1, len(intent_terms))
        if self.deterministic:
            return round(base, 4)
        return min(1.0, base + 0.05)

    def _estimate_cost(self, compressed_state: dict[str, Any] | str) -> float:
        size = len(str(compressed_state))
        return min(1.0, size / 4000.0)

    def _route_from_score(self, score: float, cache_hit: float, ctx: dict[str, Any]) -> str:
        if cache_hit >= 1.0:
            return "cache"
        if ctx.get("tool_required"):
            return "tool"
        if score >= 0.7:
            return "kvtc_only"
        if score >= 0.35:
            return "llm"
        return self.fallback_route

    def _fallback(self, reason: str, cost: float) -> dict[str, Any]:
        return {"route": self.fallback_route, "confidence": 0.0, "reason": reason, "cost_estimate": cost}
