from dataclasses import dataclass
from enum import Enum

class PromotionDecision(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"

def _status(value): return getattr(value, "value", value)

def promotion_decision(repository, commit_sha, evidence_matrix, expected_branch=None):
    gates = list(evidence_matrix)
    if any(getattr(g, "commit_sha", None) != commit_sha for g in gates):
        return PromotionDecision.BLOCK
    if expected_branch is not None and any(getattr(g, "branch", None) != expected_branch for g in gates):
        return PromotionDecision.BLOCK
    return PromotionDecision.ALLOW if gates and all(_status(g.status) == "SUCCESS" for g in gates) else PromotionDecision.BLOCK
