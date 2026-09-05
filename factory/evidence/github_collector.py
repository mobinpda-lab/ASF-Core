"""Independent GitHub evidence collector for NIRA.

Verification is derived from GitHub observations rather than a worker-provided
boolean. The collector is read-only and fail-closed when required observations
are unavailable or inconsistent.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

from factory.contracts.schema import Evidence, ObservationState
from factory.runtime.github_api import GitHubClient


@dataclass(frozen=True)
class EvidenceRequirements:
    required_workflows: tuple[str, ...] = ()
    require_commit_status: bool = True
    require_artifact: bool = False
    require_security: bool = True


def _successful(run: dict[str, Any]) -> bool:
    return run.get("status") == "completed" and run.get("conclusion") == "success"


def collect_pr_evidence(
    client: GitHubClient,
    *,
    repo: str,
    project_id: str,
    task_id: str,
    pr_number: int,
    expected_base_sha: str,
    expected_head_sha: str,
    requirements: EvidenceRequirements,
    collector_identity: str = "nira-github-evidence-collector",
) -> Evidence:
    """Observe a PR and its exact-head GitHub execution chain."""
    pr = client.pull_request(repo, pr_number)
    head = pr.get("head", {}).get("sha")
    base = pr.get("base", {}).get("sha")
    observed_base = base or ""
    observed_head = head or ""

    state = ObservationState.VERIFIED
    reasons: list[str] = []
    if observed_head != expected_head_sha:
        state = ObservationState.INVALID
        reasons.append("PR head does not equal expected head")
    if observed_base != expected_base_sha:
        state = ObservationState.INVALID
        reasons.append("PR base does not equal expected base")
    if pr.get("state") != "open":
        state = ObservationState.INVALID
        reasons.append("PR is not open")

    status = client.commit_status(repo, expected_head_sha)
    check_runs = client.check_runs(repo, expected_head_sha)
    workflow_runs = client.workflow_runs_for_head(repo, expected_head_sha).get("workflow_runs", [])

    if requirements.require_commit_status and not status.get("statuses"):
        state = ObservationState.NOT_EXPOSED if state == ObservationState.VERIFIED else state
        reasons.append("commit status chain is not exposed")

    selected_runs = [
        run for run in workflow_runs
        if not requirements.required_workflows or run.get("name") in requirements.required_workflows
    ]
    for workflow_name in requirements.required_workflows:
        matching = [run for run in selected_runs if run.get("name") == workflow_name]
        if not matching:
            state = ObservationState.NOT_EXPOSED if state == ObservationState.VERIFIED else state
            reasons.append(f"required workflow missing: {workflow_name}")
        elif not any(_successful(run) for run in matching):
            state = ObservationState.FAILED
            reasons.append(f"required workflow not successful: {workflow_name}")

    if requirements.require_security:
        security_runs = [run for run in workflow_runs if "security" in str(run.get("name", "")).lower()]
        if not any(_successful(run) for run in security_runs):
            state = ObservationState.NOT_EXPOSED if state == ObservationState.VERIFIED else state
            reasons.append("successful security workflow not independently observed")

    if requirements.require_artifact:
        successful_run = next((run for run in selected_runs if _successful(run)), None)
        artifacts = []
        if successful_run:
            artifacts = client.workflow_run_artifacts(repo, int(successful_run["id"])).get("artifacts", [])
        if not artifacts:
            state = ObservationState.NOT_EXPOSED if state == ObservationState.VERIFIED else state
            reasons.append("required artifact not observed")
    else:
        artifacts = []

    if state == ObservationState.VERIFIED and reasons:
        state = ObservationState.NOT_EXPOSED

    run_id = None
    workflow_id = None
    if selected_runs:
        selected = max(selected_runs, key=lambda run: int(run.get("id", 0)))
        run_id = int(selected["id"])
        workflow_id = str(selected.get("workflow_id") or selected.get("name") or "")

    evidence_id = sha256(
        f"{repo}:{project_id}:{task_id}:{pr_number}:{expected_head_sha}:{run_id}:{state.value}".encode()
    ).hexdigest()[:20]

    evidence = Evidence(
        evidence_id=evidence_id,
        repo=repo,
        project_id=project_id,
        task_id=task_id,
        pr_number=pr_number,
        exact_head_sha=expected_head_sha,
        base_sha=expected_base_sha,
        workflow_id=workflow_id,
        run_id=run_id,
        event="github-independent-observation",
        check_runs=tuple(check_runs.get("check_runs", [])),
        jobs=(),
        artifacts=tuple(artifacts),
        artifact_digests=tuple(
            str(item.get("digest")) for item in artifacts if item.get("digest")
        ),
        security_results=tuple(
            {"name": run.get("name"), "id": run.get("id"), "conclusion": run.get("conclusion")}
            for run in workflow_runs
            if "security" in str(run.get("name", "")).lower()
        ),
        observed_at=datetime.now(timezone.utc).isoformat(),
        observation_state=state,
        confidence="HIGH" if state == ObservationState.VERIFIED else "NONE",
        collector_identity=collector_identity,
    )
    evidence.validate()
    return evidence
