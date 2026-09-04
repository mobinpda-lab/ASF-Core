"""Canonical orchestration decision and failure classification types."""
from enum import Enum


class Decision(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    WAIT = "WAIT"
    RECOVER = "RECOVER"


class FailureClass(str, Enum):
    TRANSIENT = "TRANSIENT"
    EVIDENCE = "EVIDENCE"
    VALIDATION = "VALIDATION"
    GOVERNANCE = "GOVERNANCE"
    UNKNOWN = "UNKNOWN"
