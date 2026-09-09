"""Change impact and critical-path routing owned by NIRA."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ValidationPath(str, Enum):
    FAST = "FAST"
    HEAVY = "HEAVY"
    FULL = "FULL"


@dataclass(frozen=True)
class ImpactDecision:
    path: ValidationPath
    risk: str
    reasons: tuple[str, ...]


def decide_impact(changed_files: tuple[str, ...]) -> ImpactDecision:
    if not changed_files:
        return ImpactDecision(ValidationPath.FULL, "UNKNOWN", ("NO_CHANGED_FILES",))

    lower = tuple(p.lower() for p in changed_files)
    protected = any(
        p.startswith(".github/workflows/")
        or p.startswith("factory/registry/")
        or "security" in p
        or "permission" in p
        or "credential" in p
        for p in lower
    )
    if protected:
        return ImpactDecision(ValidationPath.FULL, "HIGH", ("CONTROL_OR_SECURITY_SURFACE",))

    docs_only = all(
        p.endswith(".md") or p.startswith("docs/") or p in {"readme.md", "license"}
        for p in lower
    )
    if docs_only:
        return ImpactDecision(ValidationPath.FAST, "LOW", ("DOCUMENTATION_ONLY",))

    tests_only = all(
        p.startswith("test/") or p.startswith("tests/") or "/test_" in p or p.endswith("_test.py")
        for p in lower
    )
    if tests_only:
        return ImpactDecision(ValidationPath.HEAVY, "MEDIUM", ("TEST_SURFACE",))

    build_or_runtime = any(
        p.endswith((".gradle", ".gradle.kts", "pubspec.yaml", "pubspec.lock", "package.json", "package-lock.json"))
        or p.startswith(("android/", "ios/", "lib/", "src/", "factory/"))
        for p in lower
    )
    if build_or_runtime:
        return ImpactDecision(ValidationPath.FULL, "HIGH", ("RUNTIME_OR_BUILD_SURFACE",))

    return ImpactDecision(ValidationPath.HEAVY, "MEDIUM", ("GENERAL_CHANGE",))
