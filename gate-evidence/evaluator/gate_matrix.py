from dataclasses import dataclass
from enum import Enum

class PromotionDecision(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"

def _status(value): return getattr(value, "value", value)

def _evaluate(gates):
    return PromotionDecision.ALLOW if gates and all(_status(g.status) == "SUCCESS" for g in gates) else PromotionDecision.BLOCK

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
    decision = _evaluate(gates)
    return PromotionResult(repository, commit_sha, decision, "all required gates SUCCESS" if decision == PromotionDecision.ALLOW else "one or more required gates unresolved or failed")
