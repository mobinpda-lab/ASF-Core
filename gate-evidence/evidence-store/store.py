from typing import Dict, List

class EvidenceStore:
    """Append-only in-memory evidence store; replacement requires a new evidence ID."""
    def __init__(self): self._records: Dict[str, object] = {}
    def append(self, evidence_id: str, record) -> None:
        if evidence_id in self._records: raise ValueError("duplicate evidence_id")
        self._records[evidence_id] = record
    def get(self, evidence_id: str): return self._records[evidence_id]
    def all(self) -> List[object]: return list(self._records.values())
