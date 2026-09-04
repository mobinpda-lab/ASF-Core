"""Fail-closed promotion matrix integration for observed CI evidence."""
from dataclasses import dataclass
from .ci_observer import EvidenceRecord, Visibility
from .provider import ObservationState


@dataclass(frozen=True)
class PromotionGate:
    gate: str
    status: Visibility
    evidence: str
    confidence: str
    decision: str


def promotion_matrix(record: EvidenceRecord, required_artifacts: bool = False) -> tuple[PromotionGate, ...]:
    provider_uncertain = record.provider_observation is not ObservationState.AVAILABLE
    safe_success = record.state is Visibility.SUCCESS and not provider_uncertain
    confidence = "HIGH" if safe_success else "LOW"
    decision = "ALLOW" if safe_success else "BLOCK"
    reason = "normalized exact-head observation"
    if provider_uncertain:
        reason = f"provider uncertainty={record.provider_observation.value}: {record.provider_reason}"
    gates = [PromotionGate("ci-evidence", record.state, reason, confidence, decision)]
    if required_artifacts and not record.artifacts:
        gates.append(PromotionGate("artifacts", Visibility.NOT_FOUND, "required artifacts absent", "LOW", "BLOCK"))
    return tuple(gates)


__all__ = ["PromotionGate", "promotion_matrix"]
