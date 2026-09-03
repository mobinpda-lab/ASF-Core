from dataclasses import dataclass
from typing import Iterable, List
from gate_evidence.collector.models import GateEvidence

@dataclass(frozen=True)
class CorrelationKey:
    repository: str
    commit_sha: str
    workflow: str = ""
    event: str = ""
    run_id: int = 0
    job_id: int = 0
    artifact_id: int = 0
    check_id: int = 0

def correlate(evidence: Iterable[GateEvidence], repository: str, commit_sha: str) -> List[GateEvidence]:
    """Return only evidence matching the exact repository and commit SHA."""
    return [item for item in evidence if item.repository == repository and item.commit_sha == commit_sha]
