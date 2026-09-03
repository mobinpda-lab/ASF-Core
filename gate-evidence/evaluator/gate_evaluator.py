from enum import Enum

class PromotionDecision(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"

def _status(value):
    return getattr(value, "value", value)

def evaluate(required_gates):
    gates = list(required_gates)
    return PromotionDecision.ALLOW if gates and all(_status(g.status) == "SUCCESS" for g in gates) else PromotionDecision.BLOCK
