from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_scheduler_is_single_lease_launch_authority():
    intake = read(".github/workflows/nira-intake-queue.yml")
    scheduler = read(".github/workflows/nira-queue-scheduler.yml")
    lease = read(".github/workflows/nira-lease.yml")

    assert "workflow_id: 'nira-queue-scheduler.yml'" in intake
    assert "workflow_id: 'nira-lease.yml'" not in intake
    assert "workflow_id: 'nira-lease.yml'" in scheduler
    assert "scheduler_run_id" in scheduler
    assert "scheduler_run_id" in lease
    assert "nira-scheduler-dispatch-v1:" in lease
    assert "UNAUTHORIZED_OR_REPLAYED_SCHEDULER_HANDOFF" in lease
    assert "issues:" not in lease.split("permissions:", 1)[0]


def test_scheduler_separates_ai_and_deterministic_capacity():
    scheduler = read(".github/workflows/nira-queue-scheduler.yml")
    assert "NIRA_AI_PROVIDER_AVAILABLE" in scheduler
    assert "activeAi" in scheduler
    assert "activeDeterministic" in scheduler
    assert "Math.max(0, 1 - activeAi)" in scheduler
    assert "Math.max(0, 4 - activeDeterministic)" in scheduler
    assert "priority:release-blocker" in scheduler
    assert "priority:core" in scheduler


def test_recovery_releases_capacity_on_pr_and_main_drift():
    recovery = read(".github/workflows/nira-recovery-sweep.yml")
    assert "NIRA_LEASE=HANDED_TO_PR" in recovery
    assert "CLIENT_MAIN_DRIFT_NO_WORKER_PR" in recovery
    assert "LEASE_TTL_EXPIRED_NO_WORKER_PR" in recovery
    assert "workflow_id: 'nira-queue-scheduler.yml'" in recovery
    assert "NIRA Cross-Repository Worker" in recovery
    assert "NIRA Deterministic Documentation Worker" in recovery


def test_failure_feedback_is_exact_head_bounded_and_scope_aware():
    feedback = read(".github/workflows/nira-failure-feedback.yml")
    assert "head_sha" in feedback
    assert "failure', 'timed_out" in feedback
    assert "conclusion === 'success' || conclusion === 'cancelled'" in feedback
    assert "NIRA_AUTO_FIX_ATTEMPT" in feedback
    assert "nextAttempt <= 2" in feedback
    assert "filename.startsWith('.github/workflows/')" in feedback
    assert "factory/registry/promotion-policy.json" in feedback
    assert "workflow_id: 'nira-intake-queue.yml'" in feedback


def test_production_orchestrator_shell_loop_stays_inside_yaml_run_block():
    orchestrator = read(".github/workflows/production-orchestrator.yml")
    assert "\n          done < <(jq -c '.[]' <<<\"$candidates\")\n" in orchestrator
    assert "\ndone < <(jq -c '.[]' <<<\"$candidates\")\n" not in orchestrator
