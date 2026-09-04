from core.evidence.ci_observer import EvidenceObserver, Visibility
from core.evidence.gate_integration import promotion_matrix

SHA = "6a26f23572a951642b4dea3b17d6a8f672b56e1f"


def test_exact_head_success_reaches_allow():
    source = {"workflow_runs": [{"repository": "org/repo", "commit_sha": SHA, "conclusion": "success"}], "check_runs": [{"repository": "org/repo", "commit_sha": SHA, "conclusion": "success"}], "jobs": [{"repository": "org/repo", "commit_sha": SHA, "conclusion": "success"}], "artifacts": [{"repository": "org/repo", "commit_sha": SHA}], "statuses": [{"repository": "org/repo", "commit_sha": SHA, "state": "success"}]}
    record = EvidenceObserver().observe("org/repo", SHA, source)
    assert record.state is Visibility.SUCCESS
    assert promotion_matrix(record)[0].decision == "ALLOW"
