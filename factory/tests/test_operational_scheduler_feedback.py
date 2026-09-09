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
    assert "maxAi" in scheduler
    assert "HEALTHY_BACKLOG" in scheduler
    assert "QUALITY_DEGRADED" in scheduler
    assert "PROVIDER_PRESSURE" in scheduler
    assert "Math.max(0, maxAi - activeAi)" in scheduler
    assert "Math.max(0, 4 - activeDeterministic)" in scheduler
    assert "activeAiRepos" in scheduler
    assert "active AI lease already owns client" in scheduler
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


def test_local_promotion_authority_does_not_depend_on_cross_repo_app():
    orchestrator = read(".github/workflows/production-orchestrator.yml")
    worker = read(".github/workflows/nira-cross-repo-worker.yml")
    assert "contents: write" in orchestrator
    assert "pull-requests: write" in orchestrator
    assert "GH_TOKEN: ${{ github.token }}" in orchestrator
    assert "Mint GitHub App installation token" not in orchestrator
    assert "NIRA_INSTALLATION_ID" not in orchestrator
    assert "actions/create-github-app-token@v2" in worker


def test_provider_pressure_releases_lease_and_scheduler_honors_cooldown():
    worker = read(".github/workflows/nira-cross-repo-worker.yml")
    scheduler = read(".github/workflows/nira-queue-scheduler.yml")
    lease = read(".github/workflows/nira-lease.yml")

    assert "control_issue_number" in lease
    assert "control_issue_number" in worker
    assert "NIRA_PROVIDER_PRESSURE_HTTP_" in worker
    assert "[429, 502, 503, 504]" in worker
    assert "NIRA_PROVIDER_COOLDOWN_UNTIL" in worker
    assert "ACTION=RELEASE_LEASE_AND_REQUEUE" in worker
    assert "PRODUCT_FAILURE_CLAIMED=false" in worker
    assert "workflow_id: 'nira-queue-scheduler.yml'" in worker
    assert "NIRA_PROVIDER_COOLDOWN_UNTIL" in scheduler
    assert "provider cooldown active until" in scheduler


def test_main_closure_revalidates_exact_final_main_without_promotion_authority():
    closure = read(".github/workflows/nira-main-closure.yml")
    assert "workflows: ['NIRA Production Orchestrator']" in closure
    assert "contents: read" in closure
    assert "contents: write" not in closure
    assert "ref: main" in closure
    assert "git rev-parse origin/main" in closure
    assert "python -m pytest -q factory/tests" in closure
    assert "nira-main-closure.json" in closure
    assert "observation_state" in closure
    assert "validator_identity" in closure
    assert "pull-requests: write" not in closure


def test_control_issue_identity_is_supported_by_both_worker_lanes():
    lease = read(".github/workflows/nira-lease.yml")
    ai_worker = read(".github/workflows/nira-cross-repo-worker.yml")
    deterministic = read(".github/workflows/nira-deterministic-doc-worker.yml")
    assert "control_issue_number: String(issue.number)" in lease
    assert "control_issue_number:" in ai_worker
    assert "control_issue_number:" in deterministic
    assert "CONTROL_ISSUE_NUMBER: ${{ inputs.control_issue_number }}" in ai_worker
    assert "CONTROL_ISSUE_NUMBER: ${{ inputs.control_issue_number }}" in deterministic


def test_worker_repairs_only_locally_invalid_model_outputs_with_bounded_budget():
    worker = read(".github/workflows/nira-cross-repo-worker.yml")
    assert "requestValidatedJson" in worker
    assert "attempt <= 2" in worker
    assert "OUTPUT_INVALID_AFTER_REPAIR" in worker
    assert "Do not broaden scope" in worker
    assert "NIRA_PROVIDER_PRESSURE_HTTP_" in worker
    assert "responses(request)" in worker
    assert "replacement payload exceeds bounded size" in worker


def test_factory_pulse_is_read_only_and_reports_operational_state_not_fake_progress():
    pulse = read(".github/workflows/nira-factory-pulse.yml")
    assert "issues: read" in pulse
    assert "pull-requests: read" in pulse
    assert "contents: read" in pulse
    assert "issues: write" not in pulse
    assert "pull-requests: write" not in pulse
    assert "mutation_authority: 'NONE'" in pulse
    assert "provider_cooldown_active" in pulse
    assert "oldest_queued_age_seconds" in pulse
    assert "authorized_candidates" in pulse
    assert "percentage" not in pulse.lower()


def test_provider_capacity_exhaustion_blocks_ai_lane_without_blind_retry():
    worker = read(".github/workflows/nira-cross-repo-worker.yml")
    scheduler = read(".github/workflows/nira-queue-scheduler.yml")
    assert "NIRA_PROVIDER_CAPACITY_EXHAUSTED" in worker
    assert "no credits remaining" in worker
    assert "provider_exhausted" in worker
    assert "ACTION=BLOCK_AI_LANE_UNTIL_CAPACITY_RESTORED" in worker
    assert "factory:blocked" in worker
    assert "providerCapacityExhausted" in scheduler
    assert "PROVIDER_CAPACITY_EXHAUSTED" in scheduler
    assert "maxAi = 0" in scheduler


def test_production_orchestrator_uses_supported_graphql_ready_transition():
    orchestrator = read(".github/workflows/production-orchestrator.yml")
    assert "markPullRequestReadyForReview" in orchestrator
    assert "gh api graphql" in orchestrator
    assert "/ready_for_review" not in orchestrator
    assert "node_id" in orchestrator


def test_recovery_has_event_driven_wakes_for_main_and_pr_closure():
    recovery = read(".github/workflows/nira-recovery-sweep.yml")
    assert "pull_request:" in recovery
    assert "types: [closed]" in recovery
    assert "push:" in recovery
    assert "branches: [main]" in recovery
    assert "NIRA_LEASE=HANDED_TO_PR" in recovery
    assert "CLIENT_MAIN_DRIFT_NO_WORKER_PR" in recovery


def test_scheduler_self_heals_nira_leases_on_main_push():
    scheduler = read(".github/workflows/nira-queue-scheduler.yml")
    assert "push:" in scheduler
    assert "branches: [main]" in scheduler
    assert "NIRA_SCHEDULER_SELF_HEAL" in scheduler
    assert "NIRA_MAIN_DRIFT" in scheduler
    assert "LEASE_TTL_EXPIRED" in scheduler
    assert "nira-scheduler-stale-lease-v1:" in scheduler
    assert "NIRA_RECOVERY=REQUEUE" in scheduler


def test_orchestrator_explicitly_wakes_canonical_scheduler():
    orchestrator = read(".github/workflows/production-orchestrator.yml")
    assert "Wake canonical queue scheduler" in orchestrator
    assert "nira-queue-scheduler.yml" in orchestrator
    assert "NIRA_SCHEDULER_WAKE=ORCHESTRATOR" in orchestrator
