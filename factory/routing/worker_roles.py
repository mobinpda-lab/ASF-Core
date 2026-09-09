"""Specialized worker role contracts for NIRA.

Roles define authority and routing boundaries. They do not create competing
execution engines; NIRA keeps canonical worker/validator/promotion authorities.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class WorkerRole(str, Enum):
    ARCHITECT = "ARCHITECT"
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    REVIEW = "REVIEW"
    DOCUMENTATION = "DOCUMENTATION"
    RELEASE = "RELEASE"
    RECOVERY = "RECOVERY"


@dataclass(frozen=True)
class RoleContract:
    role: WorkerRole
    mutation_allowed: bool
    promotion_allowed: bool
    allowed_surfaces: tuple[str, ...]
    authority: str


CONTRACTS = {
    WorkerRole.ARCHITECT: RoleContract(
        WorkerRole.ARCHITECT, False, False,
        ("analysis", "architecture-proposal", "task-decomposition"),
        "NIRA analysis only",
    ),
    WorkerRole.DEVELOPMENT: RoleContract(
        WorkerRole.DEVELOPMENT, True, False,
        ("bounded-source", "bounded-tests", "bounded-docs"),
        "NIRA Cross-Repository Worker",
    ),
    WorkerRole.TESTING: RoleContract(
        WorkerRole.TESTING, False, False,
        ("client-native-ci", "test-evidence"),
        "NIRA Client-Native Validation",
    ),
    WorkerRole.REVIEW: RoleContract(
        WorkerRole.REVIEW, False, False,
        ("security", "architecture-conformance", "exact-head-evidence"),
        "NIRA validators/gates",
    ),
    WorkerRole.DOCUMENTATION: RoleContract(
        WorkerRole.DOCUMENTATION, True, False,
        ("markdown", "generated-state"),
        "NIRA deterministic documentation/state workers",
    ),
    WorkerRole.RELEASE: RoleContract(
        WorkerRole.RELEASE, False, False,
        ("release-readiness", "release-evidence"),
        "NIRA release authority (separate from code worker)",
    ),
    WorkerRole.RECOVERY: RoleContract(
        WorkerRole.RECOVERY, False, False,
        ("failure-classification", "lease-recovery", "repair-task-generation"),
        "NIRA Recovery/Failure Feedback",
    ),
}


def infer_role(title: str, body: str = "") -> WorkerRole:
    text = f"{title}\n{body}".lower()
    if any(k in text for k in ("release", "version", "deploy", "artifact publication")):
        return WorkerRole.RELEASE
    if any(k in text for k in ("recover", "recovery", "stale lease", "auto-fix", "failure")):
        return WorkerRole.RECOVERY
    if any(k in text for k in ("review", "security", "audit", "conformance")):
        return WorkerRole.REVIEW
    if any(k in text for k in ("test", "coverage", "regression", "validation")):
        return WorkerRole.TESTING
    if any(k in text for k in ("docs", "documentation", "readme", "changelog")):
        return WorkerRole.DOCUMENTATION
    if any(k in text for k in ("architecture", "design", "schema", "api design")):
        return WorkerRole.ARCHITECT
    return WorkerRole.DEVELOPMENT
