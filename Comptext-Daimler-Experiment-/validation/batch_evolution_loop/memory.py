"""
Memory – Persistent experiment memory system.
"""

import json
import os
from typing import List, Dict, Optional

class Memory:
    def __init__(self, storage_path: str = "validation/batch_evolution_loop/history.jsonl"):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self):
        directory = os.path.dirname(self.storage_path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def save_result(self, candidate_result: Dict):
        """
        Stores candidate result.
        """
        self.append_history(candidate_result)

    def append_history(self, record: Dict):
        """
        Appends a record to the JSONL history log.
        """
        with open(self.storage_path, "a") as f:
            f.write(json.dumps(record) + "\n")

    def load_best(self) -> Optional[Dict]:
        """
        Loads the candidate with the best score from history.
        """
        if not os.path.exists(self.storage_path):
            return None

        best_candidate = None
        best_score = -float("inf")

        with open(self.storage_path, "r") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    if record.get("score", -float("inf")) > best_score:
                        best_score = record["score"]
                        best_candidate = record
                except json.JSONDecodeError:
                    continue

        return best_candidate

    def get_all_history(self) -> List[Dict]:
        history = []
        if not os.path.exists(self.storage_path):
            return history

        with open(self.storage_path, "r") as f:
            for line in f:
                try:
                    history.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return history
