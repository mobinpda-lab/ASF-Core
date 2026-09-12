from datetime import datetime, timezone

import pytest

from factory.contracts.schema import ProjectContract, TaskState, Evidence, ObservationState
from factory.gates.engine import Gate, GateResult, artifact_gate, evaluate, exact_head_gate
from factory.recovery.policy import RecoveryPolicy
from factory.runtime.state_machine import Lease, LeaseDecision, expiry_from, transition, validate_lease


def test_illegal_transition_is_fail_closed():
    with pytest.raises(ValueError):
        transition(TaskState.READY, TaskState.PROMOTED)


def test_stale_or_wrong_worker_is_rejected():
    now = datetime.now(timezone.utc)
    lease = Lease("l1", "t1", "w1", 7, now, expiry_from(now))
    assert validate_lease(lease, "w2", 7, now) == LeaseDecision.REJECT_OWNER
    assert validate_lease(lease, "w1", 8, now) == LeaseDecision.REJECT_FENCED


def test_expired_lease_is_rejected():
    now = datetime.now(timezone.utc)
    lease = Lease("l1", "t1", "w1", 7, now, now)
    assert validate_lease(lease, "w1", 7, now) == LeaseDecision.REJECT_EXPIRED


def test_gate_engine_never_promotes_on_missing_evidence():
    decision = evaluate([Gate("ci", lambda _: False)], object())
    assert decision.result == GateResult.BLOCKED
    assert decision.failed_gates == ("ci",)


def test_exact_head_and_artifact_are_explicit():
    assert exact_head_gate("a" * 40, "a" * 40)
    assert not exact_head_gate("a" * 40, "b" * 40)
    assert artifact_gate("tests", [{"name": "tests", "expired": False}])
    assert not artifact_gate("tests", [{"name": "tests", "expired": True}])


def test_evidence_requires_identity_and_confidence():
    evidence = Evidence("e1", "org/repo", "p", "t", 1, "a" * 40, "b" * 40, None, None, "ci")
    with pytest.raises(ValueError):
        evidence.validate()


def test_recovery_is_bounded():
    policy = RecoveryPolicy()
    assert policy.decision(0, True) == "REQUEUE"
    assert policy.decision(2, True) == "REQUEUE"
    assert policy.decision(3, True) == "ESCALATE"
    assert policy.decision(1, False) == "ESCALATE"


def test_self_diagnostic_reports_blocked_for_expired_lease():
    from factory.runtime.state_machine import self_diagnostic

    now = datetime.now(timezone.utc)
    lease = Lease("l1", "t1", "w1", 7, now, now)
    assert self_diagnostic(lease, now=now) == "BLOCKED"


def test_self_diagnostic_reports_healthy_for_active_lease():
    from factory.runtime.state_machine import self_diagnostic

    now = datetime.now(timezone.utc)
    lease = Lease("l1", "t1", "w1", 7, now, expiry_from(now))
    assert self_diagnostic(lease, now=now) == "HEALTHY"


def test_health_snapshot_is_deterministic_and_github_authoritative():
    from factory.nira_control_plane import NIRAControlPlane
    from factory.adapters.arvin import ArvinClientAdapter

    control = NIRAControlPlane(ArvinClientAdapter())
    snapshot = control.health_snapshot()
    assert snapshot["state"] in ("HEALTHY", "DEGRADED", "BLOCKED")
    assert snapshot["queued_tasks"] == 0
    assert snapshot["active_leases"] == 0
    assert snapshot["expired_leases"] == 0
    assert snapshot["verified_evidence"] == 0
    assert "timestamp" in snapshot
