from core.evidence.diagnostics import EvidenceSourceState, diagnose
from core.evidence.provider import ObservationState


def test_authoritative_absence_is_not_found():
    d = diagnose("o/r", "a" * 40, "github", ObservationState.AVAILABLE, {"authoritative_not_found": True})
    assert d.source_state is EvidenceSourceState.AUTHORITATIVE_NOT_FOUND
    assert d.confidence == "HIGH"


def test_connector_limit_is_not_exposed():
    d = diagnose("o/r", "a" * 40, "github", ObservationState.UNAVAILABLE, {"connector_limited": True})
    assert d.source_state is EvidenceSourceState.CONNECTOR_LIMITATION
    assert d.confidence == "LOW"


def test_known_execution_with_uncertain_observation_is_executed_not_exposed():
    d = diagnose("o/r", "a" * 40, "github", ObservationState.PARTIAL, {"execution_observed": True})
    assert d.source_state is EvidenceSourceState.EXECUTED_NOT_EXPOSED
    assert d.confidence == "LOW"


def test_empty_uncertain_payload_is_not_authoritative_absence():
    d = diagnose("o/r", "a" * 40, "github", ObservationState.UNAVAILABLE, {})
    assert d.source_state is EvidenceSourceState.OBSERVATION_UNCERTAIN
