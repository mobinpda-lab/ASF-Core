"""Current-head recovery and idempotency coverage for NIRA.

This test exercises the actual NIRA control-plane queue and lease primitives,
without mocking their behavior. It is intentionally bounded: it proves the
current in-process recovery/idempotency contracts, not persistence across a
process restart or production promotion.
"""
from datetime import datetime, timedelta, timezone

import pytest

from factory.adapters.arvin import ArvinClientAdapter
from factory.contracts.schema import Task, TaskState, idempotency_key
from factory.nira_control_plane import NIRAControlPlane
from factory.recovery.policy import RecoveryPolicy
from factory.runtime.state_machine import LeaseDecision, validate_lease


def _task(*, attempt: int = 0, base_sha: str = "a" * 40) -> Task:
    return Task(
        task_id="recovery-idempotency-001",
        project_id="arvin-clean",
        issue_ref="github:ASF-Core#47",
        objective="exercise recovery and idempotent replay",
        acceptance_criteria=("expired lease rejected", "bounded recovery", "idempotent replay"),
        base_main_sha=base_sha,
        attempt=attempt,
        idempotency_key=idempotency_key("arvin-clean", "recovery-idempotency-001", base_sha, attempt),
        state=TaskState.READY,
    )


def test_expired_lease_is_rejected_fail_closed():
    control = NIRAControlPlane(ArvinClientAdapter())
    now = datetime.now(timezone.utc)
    task = _task()
    control.intake(task)
    lease = control.lease(task, "worker-1", now=now)

    assert validate_lease(
        lease,
        "worker-1",
        lease.fence_token,
        now=lease.expires_at,
    ) == LeaseDecision.REJECT_EXPIRED


def test_recovery_policy_requeues_retryable_and_escalates_non_retryable():
    policy = RecoveryPolicy(max_attempts=3)

    assert policy.decision(0, True) == "REQUEUE"
    assert policy.decision(2, True) == "REQUEUE"
    assert policy.decision(0, False) == "ESCALATE"
    assert policy.decision(3, True) == "ESCALATE"


def test_replaying_same_idempotency_key_does_not_duplicate_queue_item():
    control = NIRAControlPlane(ArvinClientAdapter())
    first = control.intake(_task())
    second = control.intake(_task())

    assert second is first
    assert control.queue.next() is first


def test_idempotency_key_changes_when_attempt_changes():
    first = _task(attempt=0).idempotency_key
    retry = _task(attempt=1).idempotency_key

    assert first != retry


def test_expiry_boundary_is_not_accepted_even_with_correct_owner_and_fence():
    control = NIRAControlPlane(ArvinClientAdapter())
    now = datetime.now(timezone.utc)
    task = _task()
    control.intake(task)
    lease = control.lease(task, "worker-1", now=now)

    with pytest.raises(PermissionError):
        control.authorize_worker(
            task,
            lease,
            "worker-1",
            lease.fence_token,
            now=lease.expires_at + timedelta(microseconds=1),
        )
