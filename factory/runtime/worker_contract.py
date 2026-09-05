"""Fail-closed contract for a real NIRA worker handoff.

The contract carries only factory execution metadata. Product/business logic
stays in the registered client adapter/repository.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkerLeaseContext:
    task_id: str
    issue_number: int
    worker_id: str
    lease_id: str
    fence_token: int
    expected_client_sha: str
    client_repository: str

    def validate(self) -> None:
        if not self.task_id or not self.issue_number or not self.worker_id:
            raise ValueError("worker identity/task/issue are required")
        if not self.lease_id or self.fence_token <= 0:
            raise ValueError("lease and fence are required")
        if len(self.expected_client_sha) != 40:
            raise ValueError("expected client SHA must be a full commit SHA")
        if self.client_repository.count("/") != 1:
            raise ValueError("client repository must be owner/name")


class WorkerAuthorizationError(PermissionError):
    """Raised whenever a worker handoff cannot be proven safe."""


def authorize_handoff(context: WorkerLeaseContext, observed_client_sha: str) -> None:
    """Reject stale/incorrect client state before any client mutation."""
    context.validate()
    if observed_client_sha != context.expected_client_sha:
        raise WorkerAuthorizationError("CLIENT_HEAD_DRIFT")
