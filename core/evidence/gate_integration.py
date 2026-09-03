"""Fail-closed promotion matrix integration for observed CI evidence."""
from dataclasses import dataclass
from .ci_observer import EvidenceRecord, Visibility


@dataclass(frozen=True)
class PromotionGate:
    gate: str
    status: Visibility
    evidence: str
    confidence: str
    decision: str


def promotion_matrix(record: EvidenceRecord, required_artifacts: bool = False) -> tuple[PromotionGate, ...]:
    confidence = "HIGH" if record.state is Visibility.SUCCESS else "LOW"
    decision = "ALLOW" if record.state is Visibility.SUCCESS else "BLOCK"
    gates = [PromotionGate("ci-evidence", record.state, "normalized exact-head observation", confidence, decision)]
    if required_artifacts and not record.artifacts:
        gates.append(PromotionGate("artifacts", Visibility.NOT_FOUND, "required artifacts absent", "LOW", "BLOCK"))
    return tuple(gates)
