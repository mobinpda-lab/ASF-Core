"""Canonical ASF-MOC factory contracts.

The factory owns these contracts; product repositories are adapters/clients.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

SHA40 = 40


class ObservationState(str, Enum):
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    NOT_EXPOSED = "NOT_EXPOSED"
    STALE = "STALE"
    INVALID = "INVALID"


class TaskState(str, Enum):
    READY = "READY"
    LEASED = "LEASED"
    RUNNING = "RUNNING"
    VALIDATING = "VALIDATING"
    PROMOTABLE = "PROMOTABLE"
    PROMOTED = "PROMOTED"
    FAILED = "FAILED"
    ESCALATED = "ESCALATED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class ProjectContract:
    project_id: str
    repository: str
    provider: str = "github"
    default_branch: str = "main"
    enabled: bool = True
    owner: str = ""
    adapter: str = "generic"
    task_source: str = "github_issues"
    branch_policy: Mapping[str, Any] = field(default_factory=dict)
    pr_policy: Mapping[str, Any] = field(default_factory=dict)
    ci_contract: Mapping[str, Any] = field(default_factory=dict)
    required_checks: tuple[str, ...] = ()
    security_gates: tuple[str, ...] = ()
    artifact_requirements: tuple[str, ...] = ()
    promotion_policy: Mapping[str, Any] = field(default_factory=dict)
    release_policy: Mapping[str, Any] = field(default_factory=dict)
    worker_contract: Mapping[str, Any] = field(default_factory=dict)
    lease_policy: Mapping[str, Any] = field(default_factory=dict)
    retry_policy: Mapping[str, Any] = field(default_factory=dict)
    recovery_policy: Mapping[str, Any] = field(default_factory=dict)
    evidence_retention: Mapping[str, Any] = field(default_factory=dict)
    completion_definition: tuple[str, ...] = ()
    last_verified_main_sha: str | None = None
    schema_version: str = "1.0"


@dataclass(frozen=True)
class Task:
    task_id: str
    project_id: str
    issue_ref: str
    objective: str
    constraints: tuple[str, ...] = ()
    acceptance_criteria: tuple[str, ...] = ()
    base_main_sha: str = ""
    lease_id: str | None = None
    attempt: int = 0
    idempotency_key: str = ""
    priority: int = 100
    state: TaskState = TaskState.READY


@dataclass(frozen=True)
class ExecutionResult:
    task_id: str
    project_id: str
    lease_id: str
    worker_id: str
    branch: str
    base_sha: str
    result_sha: str
    changed_files: tuple[str, ...] = ()
    tests: Mapping[str, Any] = field(default_factory=dict)
    security_results: Mapping[str, Any] = field(default_factory=dict)
    failure_class: str | None = None
    attempt: int = 0
    started_at: str = ""
    completed_at: str = ""


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    repo: str
    project_id: str
    task_id: str
    pr_number: int | None
    exact_head_sha: str
    base_sha: str
    workflow_id: str | None
    run_id: int | None
    event: str
    check_runs: tuple[Mapping[str, Any], ...] = ()
    jobs: tuple[Mapping[str, Any], ...] = ()
    artifacts: tuple[Mapping[str, Any], ...] = ()
    artifact_digests: tuple[str, ...] = ()
    security_results: tuple[Mapping[str, Any], ...] = ()
    provider: str = "github"
    observed_at: str = ""
    observation_state: ObservationState = ObservationState.NOT_EXPOSED
    confidence: str = "NONE"
    collector_identity: str = ""
    schema_version: str = "1.0"

    def validate(self) -> None:
        if len(self.exact_head_sha) != SHA40:
            raise ValueError("exact_head_sha must be a 40-character SHA")
        if len(self.base_sha) != SHA40:
            raise ValueError("base_sha must be a 40-character SHA")
        if not self.collector_identity:
            raise ValueError("collector_identity is required")
        if self.observation_state == ObservationState.VERIFIED and self.confidence == "NONE":
            raise ValueError("verified evidence requires non-zero confidence")


def idempotency_key(project_id: str, task_id: str, base_sha: str, attempt: int) -> str:
    return f"{project_id}:{task_id}:{base_sha}:{attempt}"
