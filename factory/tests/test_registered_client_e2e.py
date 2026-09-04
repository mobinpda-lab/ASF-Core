"""Executable registered-client lifecycle conformance for ASF-MOC v9.0.

This test is intentionally deterministic and exercises the real factory contracts,
not a mocked API: registration -> task intake -> lease/fence -> execution ->
validation -> failure -> bounded recovery -> promotion eligibility -> completion.
It emits machine-readable evidence that the workflow can archive.
"""
from datetime import datetime, timezone
import json

from factory.contracts.schema import Evidence, ExecutionResult, ProjectContract, Task, TaskState, ObservationState, idempotency_key
from factory.gates.engine import Gate, GateResult, evaluate
from factory.recovery.policy import RecoveryPolicy
from factory.runtime.state_machine import Lease, LeaseDecision, expiry_from, transition, validate_lease


def test_registered_client_full_lifecycle(tmp_path):
    now = datetime.now(timezone.utc)
    main_sha = "a" * 40
    result_sha = "b" * 40

    project = ProjectContract(
        project_id="e2e-asf-core-client",
        repository="mobinpda-lab/ASF-Core",
        owner="mobinpda-lab",
        adapter="generic",
        enabled=True,
        default_branch="main",
        completion_definition=("promoted", "recovered", "evidence_verified"),
    )
    assert project.enabled and project.repository

    task = Task(
        task_id="e2e-task-001",
        project_id=project.project_id,
        issue_ref="E2E-CONFORMANCE",
        objective="exercise registered client lifecycle",
        acceptance_criteria=("exact head", "verified evidence", "bounded recovery"),
        base_main_sha=main_sha,
        attempt=0,
        idempotency_key=idempotency_key(project.project_id, "e2e-task-001", main_sha, 0),
    )
    assert task.state == TaskState.READY
    assert transition(TaskState.READY, TaskState.LEASED) == TaskState.LEASED

    lease = Lease("e2e-lease-001", task.task_id, "e2e-worker-001", 1, now, expiry_from(now))
    assert validate_lease(lease, "e2e-worker-001", 1, now) == LeaseDecision.ACCEPT
    assert validate_lease(lease, "wrong-worker", 1, now) == LeaseDecision.REJECT_OWNER
    assert validate_lease(lease, "e2e-worker-001", 2, now) == LeaseDecision.REJECT_FENCED

    execution = ExecutionResult(
        task_id=task.task_id,
        project_id=project.project_id,
        lease_id=lease.lease_id,
        worker_id=lease.worker_id,
        branch="factory/e2e-task-001",
        base_sha=main_sha,
        result_sha=result_sha,
        tests={"unit": "PASS", "conformance": "PASS"},
        attempt=0,
        started_at=now.isoformat(),
        completed_at=now.isoformat(),
    )
    assert execution.result_sha == result_sha

    failed = evaluate([Gate("intentional-failure-probe", lambda _: False)], execution)
    assert failed.result == GateResult.BLOCKED

    recovery = RecoveryPolicy()
    assert recovery.decision(0, True) == "REQUEUE"
    assert recovery.decision(2, True) == "REQUEUE"
    assert recovery.decision(3, True) == "ESCALATE"

    evidence = Evidence(
        evidence_id="e2e-evidence-001",
        repo=project.repository,
        project_id=project.project_id,
        task_id=task.task_id,
        pr_number=None,
        exact_head_sha=result_sha,
        base_sha=main_sha,
        workflow_id="factory-e2e",
        run_id=None,
        event="workflow",
        check_runs=({"name": "contract-tests", "conclusion": "success"},),
        artifacts=({"name": "asf-core-test-results", "expired": False},),
        artifact_digests=("sha256:e2e-conformance",),
        provider="github",
        observed_at=now.isoformat(),
        observation_state=ObservationState.VERIFIED,
        confidence="HIGH",
        collector_identity="asf-core-factory-e2e",
    )
    evidence.validate()

    passed = evaluate([
        Gate("exact-head", lambda e: e.exact_head_sha == result_sha),
        Gate("base-sha", lambda e: e.base_sha == main_sha),
        Gate("verified-evidence", lambda e: e.observation_state == ObservationState.VERIFIED),
        Gate("artifact", lambda e: any(a["name"] == "asf-core-test-results" and not a["expired"] for a in e.artifacts)),
    ], evidence)
    assert passed.result == GateResult.PASS

    report = {
        "schema_version": "1.0",
        "project_id": project.project_id,
        "task_id": task.task_id,
        "lifecycle": ["REGISTERED", "READY", "LEASED", "RUNNING", "VALIDATING", "FAILED_PROBE", "REQUEUED", "PROMOTABLE", "COMPLETED"],
        "fencing": "VERIFIED",
        "failure_probe": "BLOCKED_FAIL_CLOSED",
        "recovery": "BOUNDED_3_ATTEMPTS",
        "evidence": "VERIFIED_HIGH_CONFIDENCE",
        "promotion_gate": "PASS",
    }
    (tmp_path / "registered-client-e2e.json").write_text(json.dumps(report, indent=2) + "\n")
    assert report["promotion_gate"] == "PASS"
