import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("gate_observability", Path(__file__).with_name("observability.py"))
_obs = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_obs)

def from_gate_evidence(evidence, gate_name):
    status = getattr(evidence.status, "value", evidence.status)
    if status == "NOT_EXPOSED":
        visibility, reason = _obs.VisibilityState.WORKFLOW_NOT_VISIBLE, "source may exist but current observer cannot expose it"
    elif status == "NOT_FOUND":
        visibility, reason = _obs.VisibilityState.EVIDENCE_INCOMPLETE, "authoritative source returned no matching evidence"
    elif getattr(evidence, "check_id", None) is not None:
        visibility, reason = _obs.VisibilityState.CHECK_VISIBLE, "check evidence is visible for the exact SHA"
    else:
        visibility, reason = _obs.VisibilityState.WORKFLOW_VISIBLE, "workflow evidence is visible for the exact SHA"
    confidence = _obs.ObservationConfidence.HIGH if status in {"SUCCESS", "FAILURE", "PENDING"} else _obs.ObservationConfidence.LOW
    return _obs.FactoryObservation(
        repository=evidence.repository,
        commit_sha=evidence.commit_sha,
        gate_name=gate_name,
        workflow_identity=evidence.workflow,
        event_type=evidence.event,
        run_id=evidence.run_id,
        check_id=getattr(evidence, "check_id", None),
        job_results=evidence.jobs,
        artifact_results=evidence.artifacts,
        visibility_state=visibility,
        confidence=confidence,
        timestamp=evidence.timestamp,
        reason=reason,
        status=_obs.ObservationStatus(status),
    )
