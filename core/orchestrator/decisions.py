from enum import Enum


class Decision(str, Enum):
    ALLOW = "ALLOW"
    WAIT = "WAIT"
    RECOVER = "RECOVER"
    BLOCK = "BLOCK"


class FailureClass(str, Enum):
    TRANSIENT = "TRANSIENT"
    EVIDENCE = "EVIDENCE"
    VALIDATION = "VALIDATION"
    GOVERNANCE = "GOVERNANCE"
    UNKNOWN = "UNKNOWN"


__all__ = ["Decision", "FailureClass"]
