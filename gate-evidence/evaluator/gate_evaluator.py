from enum import Enum
from typing import Iterable
from gate_evidence.collector.models import GateEvidence, EvidenceStatus

class PromotionDecision(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"

def evaluate(required_gates: Iterable[GateEvidence]) -> PromotionDecision:
    gates = list(required_gates)
    if gates and all(g.status == EvidenceStatus.SUCCESS for g in gates):
        return PromotionDecision.ALLOW
    return PromotionDecision.BLOCK
