from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional
import re

class VisibilityState(str, Enum):
    WORKFLOW_VISIBLE = "WORKFLOW_VISIBLE"
    WORKFLOW_NOT_VISIBLE = "WORKFLOW_NOT_VISIBLE"
    CHECK_VISIBLE = "CHECK_VISIBLE"
    CHECK_NOT_VISIBLE = "CHECK_NOT_VISIBLE"
    EVIDENCE_COMPLETE = "EVIDENCE_COMPLETE"
    EVIDENCE_INCOMPLETE = "EVIDENCE_INCOMPLETE"

class ObservationConfidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass(frozen=True)
class FactoryObservation:
    repository: str
    commit_sha: str
    gate_name: str
    workflow_identity: Optional[str] = None
    event_type: Optional[str] = None
    run_id: Optional[int] = None
    check_id: Optional[int] = None
    job_results: tuple = ()
    artifact_results: tuple = ()
    visibility_state: VisibilityState = VisibilityState.EVIDENCE_INCOMPLETE
    confidence: ObservationConfidence = ObservationConfidence.LOW
    timestamp: str = ""
    reason: str = ""

    def __post_init__(self):
        if not re.fullmatch(r"[0-9a-fA-F]{40}", self.commit_sha):
            raise ValueError("commit_sha must be a 40-character hexadecimal SHA")

    def normalized(self) -> dict:
        return self.__dict__ | {"visibility_state": self.visibility_state.value, "confidence": self.confidence.value}

def build_promotion_matrix(observations: Iterable[FactoryObservation], repository: str, commit_sha: str, required_gates: Iterable[str]) -> dict:
    rows = []
    for gate in required_gates:
        matches = [o for o in observations if o.repository == repository and o.commit_sha == commit_sha and o.gate_name == gate]
        if not matches:
            rows.append({"gate_name": gate, "status": "NOT_FOUND", "reason": "no authoritative observation for exact repository and SHA"})
            continue
        if any(o.visibility_state in {VisibilityState.WORKFLOW_NOT_VISIBLE, VisibilityState.CHECK_NOT_VISIBLE, VisibilityState.EVIDENCE_INCOMPLETE} for o in matches):
            rows.append({"gate_name": gate, "status": "NOT_EXPOSED", "reason": "required evidence is not fully observable"})
            continue
        rows.append({"gate_name": gate, "status": "SUCCESS", "reason": "observable evidence complete"})
    return {"repository": repository, "commit_sha": commit_sha, "gates": rows, "decision": "ALLOW" if rows and all(r["status"] == "SUCCESS" for r in rows) else "BLOCK"}
