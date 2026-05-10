from src.core.memory.kvtc_memory import KVTCPersistentMemory


def test_memory_recall_and_merge():
    mem = KVTCPersistentMemory()
    mem.store_state({"id": "1", "intent": "misfire", "status": "open"})
    mem.store_state({"id": "2", "intent": "brake", "status": "critical"})
    hits = mem.retrieve_relevant("brake critical")
    assert hits and hits[0]["id"] == "2"

    merged = mem.merge_states({"a": 1, "b": {"c": 2}}, {"b": {"d": 3}})
    assert merged["b"]["c"] == 2 and merged["b"]["d"] == 3
