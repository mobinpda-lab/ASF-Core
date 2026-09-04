"""GitHub provider adapter normalization with fail-closed diagnostics."""
from dataclasses import dataclass
from typing import Any, Mapping

from .provider import ObservationState, ProviderObservation


@dataclass(frozen=True)
class GitHubAdapter:
    """Adapts a provider response into the provider-independent contract."""

    def observe(self, repository: str, commit_sha: str, source: Mapping[str, Any]) -> ProviderObservation:
        self._validate_commit_sha(commit_sha)
        if source.get("accessible") is False:
            return self._result(ObservationState.UNAVAILABLE, "LOW", "provider access unavailable", source)

        required = ("workflow_runs", "check_runs", "jobs", "artifacts", "statuses")
        present = {name for name in required if name in source}
        if not present:
            return self._result(ObservationState.UNAVAILABLE, "LOW", "provider returned no observable sections", source)
        missing = set(required) - present
        values = {name: tuple(source.get(name) or ()) for name in required}

        for group in values.values():
            for item in group:
                self._validate_item(repository, commit_sha, item)

        if source.get("delayed") is True or source.get("retry_after") is not None:
            return self._result(ObservationState.DELAYED, "LOW", "provider data is delayed", values)
        if source.get("inconsistent") is True:
            return self._result(ObservationState.INCONSISTENT, "LOW", "provider response is internally inconsistent", values)
        if missing:
            return self._result(ObservationState.PARTIAL, "LOW", "missing sections: " + ", ".join(sorted(missing)), values)
        return self._result(ObservationState.AVAILABLE, "HIGH", "all provider evidence sections observable", values)

    @staticmethod
    def _validate_commit_sha(commit_sha: str) -> None:
        if len(commit_sha) != 40 or any(c not in "0123456789abcdef" for c in commit_sha.lower()):
            raise ValueError("commit_sha must be a 40-character hexadecimal SHA")

    @staticmethod
    def _validate_item(repository: str, commit_sha: str, item: Mapping[str, Any]) -> None:
        observed_repository = item.get("repository")
        if observed_repository not in (None, repository):
            raise ValueError("evidence repository mismatch")
        observed_sha = item.get("commit_sha") or item.get("head_sha")
        if observed_sha not in (None, commit_sha):
            raise ValueError("stale or mismatched commit SHA")

    @staticmethod
    def _result(state: ObservationState, confidence: str, reason: str, data: Mapping[str, Any]) -> ProviderObservation:
        normalized = {k: tuple(v or ()) for k, v in data.items() if k in {"workflow_runs", "check_runs", "jobs", "artifacts", "statuses"}}
        return ProviderObservation(state, confidence, reason, normalized)


__all__ = ["GitHubAdapter"]
