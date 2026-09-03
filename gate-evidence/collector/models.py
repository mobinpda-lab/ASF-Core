from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional
import re

class EvidenceStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PENDING = "PENDING"
    NOT_FOUND = "NOT_FOUND"
    NOT_EXPOSED = "NOT_EXPOSED"

@dataclass(frozen=True)
class GateEvidence:
    repository: str
    commit_sha: str
    workflow: Optional[str] = None
    event: Optional[str] = None
    run_id: Optional[int] = None
    job_id: Optional[int] = None
    artifact_id: Optional[int] = None
    check_id: Optional[int] = None
    checks: tuple = ()
    jobs: tuple = ()
    artifacts: tuple = ()
    conclusion: Optional[str] = None
    timestamp: str = ""
    status: EvidenceStatus = EvidenceStatus.NOT_FOUND
    branch: Optional[str] = None
    evidence_source: Optional[str] = None

    def __post_init__(self):
        if not re.fullmatch(r"[0-9a-fA-F]{40}", self.commit_sha):
            raise ValueError("commit_sha must be a 40-character hexadecimal SHA")

    def normalized(self) -> dict:
        return {"commit_sha": self.commit_sha, "workflow": self.workflow, "event": self.event, "run_id": self.run_id, "checks": list(self.checks), "jobs": list(self.jobs), "artifacts": list(self.artifacts), "conclusion": self.conclusion, "timestamp": self.timestamp, "decision": self.status.value}

def status_from_conclusion(conclusion: Any, exposed: bool = True) -> EvidenceStatus:
    if not exposed: return EvidenceStatus.NOT_EXPOSED
    if conclusion is None: return EvidenceStatus.NOT_FOUND
    value = str(conclusion).lower()
    if value in {"success", "successful"}: return EvidenceStatus.SUCCESS
    if value in {"failure", "failed", "cancelled", "timed_out", "action_required"}: return EvidenceStatus.FAILURE
    if value in {"queued", "in_progress", "pending", "waiting"}: return EvidenceStatus.PENDING
    return EvidenceStatus.NOT_FOUND

class WorkflowRunCollector:
    def collect(self, repository, commit_sha): raise NotImplementedError
class CheckRunCollector:
    def collect(self, repository, commit_sha): raise NotImplementedError
class JobResultCollector:
    def collect(self, repository, run_id): raise NotImplementedError
class ArtifactResultCollector:
    def collect(self, repository, run_id): raise NotImplementedError
