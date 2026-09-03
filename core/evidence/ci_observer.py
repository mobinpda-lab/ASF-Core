"""Normalized, fail-closed CI/CD evidence observation model."""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping

from .provider import ObservationState, ProviderObservation


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
    provider_observation: ObservationState = ObservationState.AVAILABLE
    provider_confidence: str = "HIGH"
    provider_reason: str = ""


class EvidenceObserver:
    """Correlates authoritative observations to one exact repository/SHA."""

    def observe(self, repository: str, commit_sha: str, source: Mapping[str, Any]) -> EvidenceRecord:
        self._validate_sha(commit_sha)
        if source.get("accessible") is False:
            return self._record(repository, commit_sha, {}, Visibility.NOT_EXPOSED, ObservationState.UNAVAILABLE, "LOW", "provider access unavailable")
        sections = ("workflow_runs", "check_runs", "jobs", "artifacts", "statuses")
        values = {name: tuple(source.get(name) or ()) for name in sections}
        self._reject_mismatch(repository, commit_sha, values.values())
        provider_state = ObservationState.AVAILABLE
        if source.get("delayed") is True or source.get("retry_after") is not None:
            provider_state = ObservationState.DELAYED
        elif source.get("inconsistent") is True:
            provider_state = ObservationState.INCONSISTENT
        elif any(name not in source for name in sections):
            provider_state = ObservationState.PARTIAL
        state = self._classify(values, authoritative_not_found=source.get("authoritative_not_found") is True)
        if provider_state is not ObservationState.AVAILABLE:
            state = Visibility.NOT_EXPOSED if provider_state in {ObservationState.UNAVAILABLE, ObservationState.INCONSISTENT} else Visibility.PENDING
        return EvidenceRecord(repository, commit_sha, *(values[name] for name in sections), state, provider_state, "HIGH" if provider_state is ObservationState.AVAILABLE else "LOW", provider_state.value.lower())

    def observe_provider(self, repository: str, commit_sha: str, observation: ProviderObservation) -> EvidenceRecord:
        self._validate_sha(commit_sha)
        if observation.observation is not ObservationState.AVAILABLE:
            state = Visibility.NOT_EXPOSED if observation.observation in {ObservationState.UNAVAILABLE, ObservationState.INCONSISTENT, ObservationState.PARTIAL} else Visibility.PENDING
            return self._record(repository, commit_sha, observation.data, state, observation.observation, observation.confidence, observation.reason)
        values = {name: tuple(observation.data.get(name) or ()) for name in ("workflow_runs", "check_runs", "jobs", "artifacts", "statuses")}
        self._reject_mismatch(repository, commit_sha, values.values())
        return self._record(repository, commit_sha, values, self._classify(values, authoritative_not_found=observation.data.get("authoritative_not_found") is True), observation.observation, observation.confidence, observation.reason)

    @staticmethod
    def _record(repository: str, commit_sha: str, values: Mapping[str, Any], state: Visibility, provider: ObservationState, confidence: str, reason: str) -> EvidenceRecord:
        names = ("workflow_runs", "check_runs", "jobs", "artifacts", "statuses")
        normalized = {n: tuple(values.get(n) or ()) for n in names}
        return EvidenceRecord(repository, commit_sha, *(normalized[n] for n in names), state, provider, confidence, reason)

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
    def _classify(values: Mapping[str, tuple[Mapping[str, Any], ...]], authoritative_not_found: bool = False) -> Visibility:
        runs, checks, jobs = values["workflow_runs"], values["check_runs"], values["jobs"]
        if not runs and not checks and not jobs and not values["statuses"]:
            return Visibility.NOT_FOUND if authoritative_not_found else Visibility.NOT_EXPOSED
        conclusions = [str(x.get("conclusion", "")).lower() for x in (*runs, *checks, *jobs)]
        if any(c in {"failure", "cancelled", "timed_out", "action_required"} for c in conclusions):
            return Visibility.FAILURE
        if any(c in {"", "queued", "in_progress", "pending", "waiting"} for c in conclusions):
            return Visibility.PENDING
        return Visibility.SUCCESS
