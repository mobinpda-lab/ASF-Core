from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_failure_feedback_classifies_before_auto_fix():
    wf = read(".github/workflows/nira-failure-feedback.yml")
    assert "listJobsForWorkflowRun" in wf
    assert "NIRA_FEEDBACK_CLASS" in wf
    assert "CREDENTIAL_OR_SECURITY" in wf
    assert "ENVIRONMENT_RECOVERY" in wf
    assert "BOUNDED_REPAIR" in wf
    assert "classAutoRepair && !unsafe && nextAttempt <= 2" in wf


def test_scheduler_uses_live_health_for_capacity_and_same_client_guard():
    wf = read(".github/workflows/nira-queue-scheduler.yml")
    assert "HEALTHY_BACKLOG_HIGH" in wf
    assert "QUALITY_DEGRADED" in wf
    assert "providerPressure" in wf
    assert "successRate" in wf
    assert "activeAiRepos" in wf
    assert "active AI lease already owns client" in wf


def test_change_impact_workflow_is_read_only_exact_head_evidence():
    wf = read(".github/workflows/nira-impact-plan.yml")
    assert "NIRA Change Impact Plan" in wf
    assert "factory.routing.impact" in wf
    assert "nira-impact-plan.json" in wf
    assert "promotion_authority" in wf
    assert "contents: read" in wf
    assert "pulls.merge" not in wf
    assert "createOrUpdateFileContents" not in wf
