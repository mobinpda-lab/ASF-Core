from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class EvidenceState(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PENDING = "PENDING"
    NOT_FOUND = "NOT_FOUND"
    NOT_EXPOSED = "NOT_EXPOSED"


@dataclass(frozen=True)
class GateEvaluation:
    gate_id: str
    commit_sha: str
    state: EvidenceState
    evidence_refs: tuple[str, ...] = ()
    blocking_reason: str | None = None


@dataclass(frozen=True)
class PromotionDecision:
    decision: str
    commit_sha: str
    gates: tuple[GateEvaluation, ...]


def evaluate(commit_sha: str, required_gates: Iterable[str], evidence: Iterable[GateEvaluation]) -> PromotionDecision:
    by_gate = {item.gate_id: item for item in evidence}
    gates = tuple(
        by_gate.get(
            gate,
            GateEvaluation(gate, commit_sha, EvidenceState.NOT_FOUND, blocking_reason="required gate has no evidence"),
        )
        for gate in required_gates
    )
    if any(item.commit_sha != commit_sha for item in gates):
        return PromotionDecision("BLOCK", commit_sha, gates)
    decision = "ALLOW" if gates and all(item.state is EvidenceState.SUCCESS for item in gates) else "BLOCK"
    return PromotionDecision(decision, commit_sha, gates)
