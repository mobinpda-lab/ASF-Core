import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_provider_capacity_probe_is_event_driven_five_minute_fail_closed_self_completion_only():
    workflow = read(".github/workflows/nira-provider-capacity-probe.yml")
    assert "issues:" in workflow
    assert "types: [labeled]" in workflow
    assert "cron: '*/5 * * * *'" in workflow
    assert "contents: read" in workflow
    assert "contents: write" not in workflow
    assert "NIRA_SELF_COMPLETION_TASK: true" in workflow
    assert "factory:blocked" in workflow
    assert "NIRA_PROVIDER_CAPACITY=EXHAUSTED" in workflow
    assert "NIRA_PROVIDER_CAPACITY=RESTORED" in workflow
    assert "UNBLOCK_AND_REQUEUE_SELF_COMPLETION" in workflow
    assert "nira-queue-scheduler.yml" in workflow
    assert "pulls.merge" not in workflow
    assert "createOrUpdateFileContents" not in workflow


def test_provider_probe_writes_fresh_restoration_evidence_after_new_exhaustion():
    workflow = read(".github/workflows/nira-provider-capacity-probe.yml")
    assert "latestRestored" in workflow
    assert "currentExhausted" in workflow
    assert "new Date(latestRestored.created_at) < new Date(currentExhausted.created_at)" in workflow
    assert "'PROVIDER=' + probe.provider" in workflow
    assert "'MODEL=' + (probe.model || '')" in workflow


def test_scheduler_uses_latest_capacity_event_not_any_historical_exhaustion():
    scheduler = read(".github/workflows/nira-queue-scheduler.yml")
    assert "latestCapacityEvent" in scheduler
    assert "NIRA_PROVIDER_CAPACITY=(EXHAUSTED|RESTORED)" in scheduler
    assert "latestCapacityEvent?.body?.includes('NIRA_PROVIDER_CAPACITY=EXHAUSTED')" in scheduler
    assert "comments.some(c => c.body?.includes('NIRA_PROVIDER_CAPACITY=EXHAUSTED'))" not in scheduler


def test_provider_probe_is_protected_factory_authority():
    policy = json.loads(read("factory/registry/autonomous-mutation-policy.json"))
    assert ".github/workflows/nira-provider-capacity-probe.yml" in policy["protected_paths"]
    assert policy["safety"]["provider_capacity_restoration_requires_probe_evidence"] is True
    assert policy["safety"]["provider_capacity_restoration_requeues_only_blocked_self_completion"] is True
