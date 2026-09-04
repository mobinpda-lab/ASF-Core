import pytest
from core.evidence.ci_observer import EvidenceObserver, Visibility

SHA = "6a26f23572a951642b4dea3b17d6a8f672b56e1f"


def test_successful_workflow_evidence():
    source = {"workflow_runs": [{"commit_sha": SHA, "conclusion": "success"}], "check_runs": [{"commit_sha": SHA, "conclusion": "success"}], "jobs": [{"commit_sha": SHA, "conclusion": "success"}], "artifacts": [{"commit_sha": SHA}], "statuses": [{"commit_sha": SHA, "state": "success"}]}
    assert EvidenceObserver().observe("org/repo", SHA, source).state is Visibility.SUCCESS


def test_missing_workflow_is_not_exposed_without_authoritative_absence():
    assert EvidenceObserver().observe("org/repo", SHA, {}).state is Visibility.NOT_EXPOSED


def test_authoritative_missing_workflow_is_not_found():
    source = {"authoritative_not_found": True}
    assert EvidenceObserver().observe("org/repo", SHA, source).state is Visibility.NOT_FOUND


def test_inaccessible_workflow_is_not_exposed():
    assert EvidenceObserver().observe("org/repo", SHA, {"accessible": False}).state is Visibility.NOT_EXPOSED


def test_empty_status_does_not_create_not_found_without_authoritative_absence():
    record = EvidenceObserver().observe("org/repo", SHA, {"statuses": []})
    assert record.state is Visibility.NOT_EXPOSED


def test_stale_sha_rejected():
    with pytest.raises(ValueError, match="SHA"):
        EvidenceObserver().observe("org/repo", SHA, {"workflow_runs": [{"commit_sha": "0" * 40, "conclusion": "success"}]})


def test_partial_evidence_is_pending():
    record = EvidenceObserver().observe("org/repo", SHA, {"workflow_runs": [{"commit_sha": SHA, "conclusion": "in_progress"}]})
    assert record.state is Visibility.PENDING


def test_artifact_missing_does_not_create_success():
    record = EvidenceObserver().observe("org/repo", SHA, {"workflow_runs": [{"commit_sha": SHA, "conclusion": "success"}], "check_runs": [{"commit_sha": SHA, "conclusion": "success"}], "jobs": [{"commit_sha": SHA, "conclusion": "success"}]})
    assert record.state is Visibility.SUCCESS
    assert record.artifacts == ()


def test_false_success_prevention_on_failure():
    record = EvidenceObserver().observe("org/repo", SHA, {"workflow_runs": [{"commit_sha": SHA, "conclusion": "failure"}]})
    assert record.state is Visibility.FAILURE
