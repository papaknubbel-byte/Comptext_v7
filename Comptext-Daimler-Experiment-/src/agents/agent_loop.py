from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from src.core.routing.decision_engine import DecisionEngine
from src.core.memory.kvtc_memory import KVTCPersistentMemory
from src.interpretability.decision_trace import DecisionTrace, DecisionStep
from src.interpretability.reasoning_graph import ReasoningGraph


@dataclass
class AgentLoopConfig:
    max_iterations: int = 5
    confidence_threshold: float = 0.8


class AgentLoop:
    def __init__(self, router: DecisionEngine, memory: KVTCPersistentMemory, tool_executor: Callable[[str, dict[str, Any]], dict[str, Any]] | None = None, config: AgentLoopConfig | None = None) -> None:
        self.router = router
        self.memory = memory
        self.tool_executor = tool_executor
        self.config = config or AgentLoopConfig()

    def run(self, initial_state: dict[str, Any], intent: str) -> dict[str, Any]:
        trace = DecisionTrace()
        graph = ReasoningGraph()
        state = initial_state.copy()
        solved = False
        solution = ""

        for i in range(1, self.config.max_iterations + 1):
            decision = self.router.decide(state, intent, {"confidence": state.get("confidence", 0.5), "cache_hit": state.get("cache_hit", False), "tool_required": state.get("tool_required", False)})
            route = decision["route"]
            action = self._act(route, state, intent)
            observation = action.get("observation", "")
            state = self.memory.merge_states(state, action.get("delta", {}))
            self.memory.store_state({"id": f"iter_{i}", "intent": intent, "state": state})
            graph.add_transition({"id": f"s{i-1}", "state": state}, {"id": f"s{i}", "state": state}, route)
            trace.add(DecisionStep(i, route, decision["confidence"], decision["reason"], action.get("action", "none"), observation))

            if state.get("solution_found"):
                solved = True
                solution = state.get("solution", "")
                break
            if decision["confidence"] >= self.config.confidence_threshold:
                solved = True
                solution = observation or "high-confidence resolution"
                break

        return {"solved": solved, "solution": solution, **trace.as_dict(), "graph": graph.as_dict(), "final_state": state}

    def _act(self, route: str, state: dict[str, Any], intent: str) -> dict[str, Any]:
        if route == "cache":
            return {"action": "reuse_cache", "observation": "cache reused", "delta": {"solution_found": True, "solution": "cache_result"}}
        if route == "tool" and self.tool_executor:
            result = self.tool_executor(intent, state)
            return {"action": "tool_call", "observation": str(result), "delta": result}
        if route == "kvtc_only":
            return {"action": "derive_from_kvtc", "observation": "derived from compressed state", "delta": {"confidence": min(1.0, state.get("confidence", 0.5) + 0.2)}}
        return {"action": "llm_inference", "observation": "llm analyzed context", "delta": {"confidence": min(1.0, state.get("confidence", 0.5) + 0.15)}}
