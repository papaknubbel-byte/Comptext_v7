from src.core.routing.decision_engine import DecisionEngine, RoutingWeights


def test_deterministic_routing_cache_precedence():
    engine = DecisionEngine(weights=RoutingWeights(), deterministic=True)
    out = engine.decide({"frame": "misfire alert"}, "misfire", {"confidence": 0.9, "cache_hit": True})
    assert out["route"] == "cache"
    assert out["confidence"] >= 0.0
