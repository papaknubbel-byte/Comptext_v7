from src.agents.agent_loop import AgentLoop
from src.core.memory.kvtc_memory import KVTCPersistentMemory
from src.core.routing.decision_engine import DecisionEngine


def test_multi_step_reasoning_reaches_solution():
    router = DecisionEngine(deterministic=True)
    memory = KVTCPersistentMemory()

    def tool(intent, state):
        return {"solution_found": True, "solution": f"resolved:{intent}"}

    loop = AgentLoop(router, memory, tool_executor=tool)
    result = loop.run({"confidence": 0.2, "tool_required": True}, "analyze incident")
    assert result["solved"] is True
    assert "resolved:analyze incident" in str(result["solution"])
    assert len(result["steps"]) >= 1
