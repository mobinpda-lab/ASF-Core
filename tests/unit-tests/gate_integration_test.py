from core.evidence.ci_observer import EvidenceObserver, Visibility
from core.evidence.gate_integration import promotion_matrix

SHA = "6a26f23572a951642b4dea3b17d6a8f672b56e1f"


def test_unknown_evidence_blocks():
    record = EvidenceObserver().observe("org/repo", SHA, {"accessible": False})
    gates = promotion_matrix(record)
    assert gates[0].status is Visibility.NOT_EXPOSED
    assert gates[0].decision == "BLOCK"


def test_required_missing_artifact_blocks():
    source = {"workflow_runs": [{"commit_sha": SHA, "conclusion": "success"}], "check_runs": [{"commit_sha": SHA, "conclusion": "success"}], "jobs": [{"commit_sha": SHA, "conclusion": "success"}]}
    record = EvidenceObserver().observe("org/repo", SHA, source)
    gates = promotion_matrix(record, required_artifacts=True)
    assert gates[-1].status is Visibility.NOT_FOUND
    assert gates[-1].decision == "BLOCK"
