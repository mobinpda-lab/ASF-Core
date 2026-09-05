from datetime import datetime, timezone

import pytest

from factory.adapters.arvin import ArvinClientAdapter
from factory.contracts.schema import Task, TaskState
from factory.nira_control_plane import NIRAControlPlane
from factory.runtime.state_machine import LeaseDecision, validate_lease


def make_task() -> Task:
    return Task(
        task_id="arvin-e2e-001",
        project_id="arvin-clean",
        issue_ref="github:mobinpda-lab/Arvin-clean#pending-real-issue",
        objective="real client E2E validation task",
        base_main_sha="a" * 40,
        idempotency_key="arvin-clean:arvin-e2e-001:" + "a" * 40 + ":0",
    )


def test_arvin_adapter_is_declarative_and_valid():
    adapter = ArvinClientAdapter()
    adapter.validate()
    assert set(adapter.__dataclass_fields__) == adapter.allowed_fields
    assert not any("queue" in f or "worker" in f or "merge" in f or "promotion" in f
                    for f in adapter.__dataclass_fields__)


def test_control_plane_owns_queue_and_lease_and_adapter_has_no_authority():
    adapter = ArvinClientAdapter()
    cp = NIRAControlPlane(adapter)
    task = make_task()
    cp.intake(task)
    lease = cp.lease(task, "worker-1", datetime(2026, 9, 5, tzinfo=timezone.utc))
    assert lease.task_id == task.task_id
    assert validate_lease(lease, "worker-1", lease.fence_token).value == "ACCEPT"
    assert not hasattr(adapter, "merge")
    assert not hasattr(adapter, "promote")
    assert not hasattr(adapter, "enqueue")
    assert not hasattr(adapter, "lease")


def test_queue_is_idempotent():
    cp = NIRAControlPlane(ArvinClientAdapter())
    task = make_task()
    first = cp.intake(task)
    second = cp.intake(task)
    assert first is second


def test_stale_fence_is_rejected_before_worker_execution():
    cp = NIRAControlPlane(ArvinClientAdapter())
    task = make_task()
    cp.intake(task)
    lease = cp.lease(task, "worker-1")
    with pytest.raises(PermissionError, match="REJECT_FENCED"):
        cp.authorize_worker(task, lease, "worker-1", lease.fence_token + 1)


def test_gate_requires_exact_base_head_and_ci():
    cp = NIRAControlPlane(ArvinClientAdapter())
    passed = cp.gates("a" * 40, "a" * 40, "b" * 40, "b" * 40, True)
    assert passed.result.value == "PASS"
    blocked = cp.gates("a" * 40, "c" * 40, "b" * 40, "d" * 40, True)
    assert blocked.result.value == "BLOCKED"


def test_promotion_is_only_an_authorization_result_after_verified_evidence():
    cp = NIRAControlPlane(ArvinClientAdapter())
    task = make_task()
    evidence = cp.record_evidence(
        task=task,
        pr_number=1,
        base_sha="a" * 40,
        head_sha="b" * 40,
        workflow_id="ASF-Core CI",
        run_id=123,
        collector_identity="nira-evidence-collector",
        verified=True,
    )
    assert cp.promotion_gate(evidence.evidence_id) is True
    assert not hasattr(ArvinClientAdapter(), "merge")
    assert not hasattr(ArvinClientAdapter(), "promote")


def test_unverified_evidence_cannot_authorize_promotion():
    cp = NIRAControlPlane(ArvinClientAdapter())
    task = make_task()
    evidence = cp.record_evidence(
        task=task,
        pr_number=1,
        base_sha="a" * 40,
        head_sha="b" * 40,
        workflow_id="ASF-Core CI",
        run_id=124,
        collector_identity="nira-evidence-collector",
        verified=False,
    )
    assert cp.promotion_gate(evidence.evidence_id) is False
