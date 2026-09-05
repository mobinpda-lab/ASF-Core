from __future__ import annotations

import pytest

from factory.runtime.worker_contract import (
    WorkerAuthorizationError,
    WorkerLeaseContext,
    authorize_handoff,
)


def context() -> WorkerLeaseContext:
    return WorkerLeaseContext(
        task_id="task-1",
        issue_number=25,
        worker_id="worker-test",
        lease_id="lease-1",
        fence_token=1,
        expected_client_sha="a" * 40,
        client_repository="mobinpda-lab/Arvin-clean",
    )


def test_worker_handoff_accepts_exact_client_head() -> None:
    authorize_handoff(context(), "a" * 40)


def test_worker_handoff_rejects_client_head_drift() -> None:
    with pytest.raises(WorkerAuthorizationError, match="CLIENT_HEAD_DRIFT"):
        authorize_handoff(context(), "b" * 40)


def test_worker_handoff_rejects_short_sha() -> None:
    invalid = WorkerLeaseContext(
        task_id="task-1",
        issue_number=25,
        worker_id="worker-test",
        lease_id="lease-1",
        fence_token=1,
        expected_client_sha="short",
        client_repository="mobinpda-lab/Arvin-clean",
    )
    with pytest.raises(ValueError, match="full commit SHA"):
        authorize_handoff(invalid, "short")
