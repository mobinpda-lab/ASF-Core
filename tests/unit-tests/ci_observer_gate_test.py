from core.evidence.ci_observer import EvidenceObserver, Visibility
from core.evidence.gate_integration import promotion_matrix

SHA = "6a26f23572a951642b4dea3b17d6a8f672b56e1f"


def test_not_exposed_blocks():
    record = EvidenceObserver().observe("org/repo", SHA, {"accessible": False})
    assert record.state is Visibility.NOT_EXPOSED
    assert promotion_matrix(record)[0].decision == "BLOCK"


def test_failure_blocks():
    record = EvidenceObserver().observe("org/repo", SHA, {"workflow_runs": [{"commit_sha": SHA, "conclusion": "failure"}]})
    assert promotion_matrix(record)[0].decision == "BLOCK"


def test_pending_blocks():
    record = EvidenceObserver().observe("org/repo", SHA, {"workflow_runs": [{"commit_sha": SHA, "conclusion": "in_progress"}]})
    assert record.state is Visibility.PENDING
    assert promotion_matrix(record)[0].decision == "BLOCK"
