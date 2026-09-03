"""Provider-independent evidence observation contract."""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Protocol


class ObservationState(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    PARTIAL = "PARTIAL"
    DELAYED = "DELAYED"
    INCONSISTENT = "INCONSISTENT"


@dataclass(frozen=True)
class ProviderObservation:
    """Normalized provider response; uncertainty is never terminal success."""
    observation: ObservationState
    confidence: str
    reason: str
    data: Mapping[str, tuple[Mapping[str, Any], ...]]


class EvidenceProvider(Protocol):
    """External-provider contract consumed by the ASF evidence core."""
    def discover_workflows(self, repository: str, commit_sha: str) -> tuple[Mapping[str, Any], ...]: ...
    def discover_checks(self, repository: str, commit_sha: str) -> tuple[Mapping[str, Any], ...]: ...
    def discover_jobs(self, repository: str, commit_sha: str) -> tuple[Mapping[str, Any], ...]: ...
    def discover_artifacts(self, repository: str, commit_sha: str) -> tuple[Mapping[str, Any], ...]: ...
    def discover_statuses(self, repository: str, commit_sha: str) -> tuple[Mapping[str, Any], ...]: ...


def uncertainty_blocks(observation: ObservationState) -> bool:
    return observation is not ObservationState.AVAILABLE
