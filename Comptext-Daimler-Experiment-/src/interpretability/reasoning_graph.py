from __future__ import annotations

from typing import Any


class ReasoningGraph:
    def __init__(self) -> None:
        self.nodes: list[dict[str, Any]] = []
        self.edges: list[dict[str, Any]] = []

    def add_transition(self, from_node: dict[str, Any], to_node: dict[str, Any], label: str) -> None:
        self.nodes.append(from_node)
        self.nodes.append(to_node)
        self.edges.append({"from": from_node.get("id"), "to": to_node.get("id"), "label": label})

    def as_dict(self) -> dict[str, Any]:
        uniq_nodes = {n["id"]: n for n in self.nodes if "id" in n}
        return {"nodes": list(uniq_nodes.values()), "edges": self.edges}
