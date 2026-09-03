from dataclasses import dataclass
from .gate_evaluator import PromotionDecision, evaluate

@dataclass(frozen=True)
class PromotionResult:
    repository: str
    commit_sha: str
    decision: PromotionDecision
    reason: str

def evaluate_matrix(repository, commit_sha, required_gates, expected_branch=None):
    gates = list(required_gates)
    if any(getattr(g, "commit_sha", None) != commit_sha for g in gates):
        return PromotionResult(repository, commit_sha, PromotionDecision.BLOCK, "stale or mismatched SHA")
    if expected_branch is not None and any(getattr(g, "branch", None) != expected_branch for g in gates):
        return PromotionResult(repository, commit_sha, PromotionDecision.BLOCK, "wrong branch")
    decision = evaluate(gates)
    reason = "all required gates SUCCESS" if decision == PromotionDecision.ALLOW else "one or more required gates unresolved or failed"
    return PromotionResult(repository, commit_sha, decision, reason)
