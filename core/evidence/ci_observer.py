"""Normalized, fail-closed CI/CD evidence observation model.

The adapter-facing observer deliberately does not manufacture evidence. Callers
must supply authoritative source observations; missing access is NOT_EXPOSED,
while an authoritative empty source is NOT_FOUND.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping


class Visibility(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PENDING = "PENDING"
    NOT_FOUND = "NOT_FOUND"
    NOT_EXPOSED = "NOT_EXPOSED"


@dataclass(frozen=True)
class EvidenceRecord:
    repository: str
    commit_sha: str
    workflow_runs: tuple[Mapping[str, Any], ...]
    check_runs: tuple[Mapping[str, Any], ...]
    jobs: tuple[Mapping[str, Any], ...]
    artifacts: tuple[Mapping[str, Any], ...]
    statuses: tuple[Mapping[str, Any], ...]
    state: Visibility


class EvidenceObserver:
    """Correlates authoritative observations to one exact repository/SHA."""

    def observe(self, repository: str, commit_sha: str, source: Mapping[str, Any]) -> EvidenceRecord:
        self._validate_sha(commit_sha)
        if source.get("accessible") is False:
            return EvidenceRecord(repository, commit_sha, (), (), (), (), (), Visibility.NOT_EXPOSED)

        sections = ("workflow_runs", "check_runs", "jobs", "artifacts", "statuses")
        values = {name: tuple(source.get(name) or ()) for name in sections}
        self._reject_mismatch(repository, commit_sha, values.values())
        state = self._classify(values)
        return EvidenceRecord(repository, commit_sha, *(values[name] for name in sections), state)

    @staticmethod
    def _validate_sha(sha: str) -> None:
        if len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha.lower()):
            raise ValueError("commit_sha must be a 40-character hexadecimal SHA")

    @staticmethod
    def _reject_mismatch(repository: str, commit_sha: str, groups: Iterable[Iterable[Mapping[str, Any]]]) -> None:
        for group in groups:
            for item in group:
                if item.get("repository") not in (None, repository):
                    raise ValueError("evidence repository mismatch")
                observed = item.get("commit_sha") or item.get("head_sha")
                if observed not in (None, commit_sha):
                    raise ValueError("stale or mismatched commit SHA")

    @staticmethod
    def _classify(values: Mapping[str, tuple[Mapping[str, Any], ...]]) -> Visibility:
        runs = values["workflow_runs"]
        checks = values["check_runs"]
        jobs = values["jobs"]
        if not runs and not checks and not jobs and not values["statuses"]:
            return Visibility.NOT_FOUND
        conclusions = [str(x.get("conclusion", "")).lower() for x in (*runs, *checks, *jobs)]
        if any(c in {"failure", "cancelled", "timed_out", "action_required"} for c in conclusions):
            return Visibility.FAILURE
        if any(c in {"", "queued", "in_progress", "pending", "waiting"} for c in conclusions):
            return Visibility.PENDING
        return Visibility.SUCCESS
