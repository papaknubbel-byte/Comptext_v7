from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol
import copy


class MemoryBackend(Protocol):
    def save(self, key: str, value: dict[str, Any]) -> None: ...
    def load_all(self) -> dict[str, dict[str, Any]]: ...


@dataclass
class InMemoryBackend:
    storage: dict[str, dict[str, Any]] = field(default_factory=dict)

    def save(self, key: str, value: dict[str, Any]) -> None:
        self.storage[key] = copy.deepcopy(value)

    def load_all(self) -> dict[str, dict[str, Any]]:
        return copy.deepcopy(self.storage)


class KVTCPersistentMemory:
    def __init__(self, backend: MemoryBackend | None = None) -> None:
        self.backend = backend or InMemoryBackend()
        self._states = self.backend.load_all()

    def store_state(self, state: dict[str, Any]) -> str:
        key = str(state.get("id") or f"state_{len(self._states)+1}")
        self._states[key] = copy.deepcopy(state)
        self.backend.save(key, state)
        return key

    def retrieve_relevant(self, intent: str) -> list[dict[str, Any]]:
        terms = {t.lower() for t in intent.split() if t}
        scored: list[tuple[int, dict[str, Any]]] = []
        for state in self._states.values():
            hay = str(state).lower()
            score = sum(1 for t in terms if t in hay)
            if score:
                scored.append((score, copy.deepcopy(state)))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored]

    def merge_states(self, base: dict[str, Any], delta: dict[str, Any]) -> dict[str, Any]:
        merged = copy.deepcopy(base)
        for k, v in delta.items():
            if isinstance(v, dict) and isinstance(merged.get(k), dict):
                merged[k] = self.merge_states(merged[k], v)
            else:
                merged[k] = copy.deepcopy(v)
        return merged

    def reconstruct_state(self, base: dict[str, Any], deltas: list[dict[str, Any]]) -> dict[str, Any]:
        state = copy.deepcopy(base)
        for delta in deltas:
            state = self.merge_states(state, delta)
        return state
