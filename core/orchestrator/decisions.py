from enum import Enum

class Decision(str, Enum):
    ALLOW="ALLOW"; BLOCK="BLOCK"; WAIT="WAIT"; RECOVER="RECOVER"

class FailureClass(str, Enum):
    TRANSIENT="TRANSIENT"; EVIDENCE="EVIDENCE"; VALIDATION="VALIDATION"; GOVERNANCE="GOVERNANCE"; UNKNOWN="UNKNOWN"

def decide(*, evidence_complete=False, evidence_failed=False, recoverable=False, dependencies_ready=True):
    if not dependencies_ready: return Decision.WAIT
    if evidence_failed: return Decision.RECOVER if recoverable else Decision.BLOCK
    if not evidence_complete: return Decision.WAIT
    return Decision.ALLOW
