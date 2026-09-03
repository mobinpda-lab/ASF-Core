from dataclasses import dataclass
from typing import Iterable
from .gate_evaluator import evaluate, PromotionDecision

@dataclass(frozen=True)
class PromotionResult:
    repository: str
    commit_sha: str
    decision: PromotionDecision
    reason: str

def evaluate_matrix(repository: str, commit_sha: str, required_gates: Iterable, expected_branch: str = None) -> PromotionResult:
    gates=list(required_gates)
    decision=evaluate(gates)
    reason='all required gates SUCCESS' if decision == PromotionDecision.ALLOW else 'one or more required gates unresolved or failed'
    return PromotionResult(repository, commit_sha, decision, reason)
