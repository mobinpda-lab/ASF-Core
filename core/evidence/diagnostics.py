"""Deterministic diagnostics for CI evidence provider visibility.

This module distinguishes authoritative absence from an observation-path
limitation. It never promotes uncertainty to successful evidence.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .provider import ObservationState


class EvidenceSourceState(str, Enum):
    AUTHORITATIVE_NOT_FOUND = "AUTHORITATIVE_NOT_FOUND"
    EXECUTED_NOT_EXPOSED = "CI_EXECUTED_NOT_EXPOSED"
    CONNECTOR_LIMITATION = "CONNECTOR_OBSERVATION_LIMITATION"
    OBSERVATION_AVAILABLE = "OBSERVATION_AVAILABLE"
    OBSERVATION_UNCERTAIN = "OBSERVATION_UNCERTAIN"


@dataclass(frozen=True)
class ObservationDiagnostic:
    repository: str
    commit_sha: str
    provider_source: str
    source_state: EvidenceSourceState
    observation_state: ObservationState
    confidence: str
    reason: str


def diagnose(
    repository: str,
    commit_sha: str,
    provider_source: str,
    observation: ObservationState,
    data: Mapping[str, Any],
) -> ObservationDiagnostic:
    """Classify what can be proven from an observation payload.

    NOT_FOUND is emitted only when the provider explicitly attests that the
    queried CI source was searched and no matching execution exists. Empty
    connector payloads, missing sections, and access failures remain
    observation limitations.
    """
    explicit_absence = data.get("authoritative_not_found") is True
    connector_limited = data.get("connector_limited") is True
    execution_known = data.get("execution_observed") is True

    if explicit_absence and observation is ObservationState.AVAILABLE:
        return ObservationDiagnostic(repository, commit_sha, provider_source,
            EvidenceSourceState.AUTHORITATIVE_NOT_FOUND, observation, "HIGH",
            "provider explicitly attests authoritative absence")
    if connector_limited:
        return ObservationDiagnostic(repository, commit_sha, provider_source,
            EvidenceSourceState.CONNECTOR_LIMITATION, observation, "LOW",
            "connector cannot expose the authoritative observation path")
    if execution_known and observation is not ObservationState.AVAILABLE:
        return ObservationDiagnostic(repository, commit_sha, provider_source,
            EvidenceSourceState.EXECUTED_NOT_EXPOSED, observation, "LOW",
            "execution is known but evidence is not exposed")
    if observation is ObservationState.AVAILABLE:
        return ObservationDiagnostic(repository, commit_sha, provider_source,
            EvidenceSourceState.OBSERVATION_AVAILABLE, observation, "HIGH",
            "authoritative observation is available")
    return ObservationDiagnostic(repository, commit_sha, provider_source,
        EvidenceSourceState.OBSERVATION_UNCERTAIN, observation, "LOW",
        "provider observation is uncertain")
