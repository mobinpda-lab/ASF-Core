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

class ObservationStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PENDING = "PENDING"
    NOT_FOUND = "NOT_FOUND"
    NOT_EXPOSED = "NOT_EXPOSED"

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
    status: ObservationStatus = ObservationStatus.NOT_FOUND

    def __post_init__(self):
        if not re.fullmatch(r"[0-9a-fA-F]{40}", self.commit_sha):
            raise ValueError("commit_sha must be a 40-character hexadecimal SHA")

    def normalized(self) -> dict:
        return self.__dict__ | {"visibility_state": self.visibility_state.value, "confidence": self.confidence.value, "status": self.status.value}

def build_promotion_matrix(observations: Iterable[FactoryObservation], repository: str, commit_sha: str, required_gates: Iterable[str]) -> dict:
    rows = []
    for gate in required_gates:
        matches = [o for o in observations if o.repository == repository and o.commit_sha == commit_sha and o.gate_name == gate]
        if not matches:
            rows.append({"gate_name": gate, "status": ObservationStatus.NOT_FOUND.value, "reason": "no authoritative observation for exact repository and SHA"})
            continue
        if any(o.visibility_state in {VisibilityState.WORKFLOW_NOT_VISIBLE, VisibilityState.CHECK_NOT_VISIBLE, VisibilityState.EVIDENCE_INCOMPLETE} for o in matches):
            rows.append({"gate_name": gate, "status": ObservationStatus.NOT_EXPOSED.value, "reason": "required evidence is not fully observable"})
            continue
        statuses = {o.status for o in matches}
        if statuses == {ObservationStatus.SUCCESS}:
            rows.append({"gate_name": gate, "status": ObservationStatus.SUCCESS.value, "reason": "observable evidence complete"})
        else:
            status = next((s.value for s in (ObservationStatus.FAILURE, ObservationStatus.PENDING, ObservationStatus.NOT_EXPOSED, ObservationStatus.NOT_FOUND) if s in statuses), ObservationStatus.NOT_EXPOSED.value)
            rows.append({"gate_name": gate, "status": status, "reason": "observable gate evidence is not successful"})
    return {"repository": repository, "commit_sha": commit_sha, "gates": rows, "decision": "ALLOW" if rows and all(r["status"] == ObservationStatus.SUCCESS.value for r in rows) else "BLOCK"}
