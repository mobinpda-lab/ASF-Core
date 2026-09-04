import pytest
from core.evidence.ci_observer import EvidenceObserver

SHA = "6a26f23572a951642b4dea3b17d6a8f672b56e1f"


def test_wrong_repository_rejected():
    with pytest.raises(ValueError, match="repository"):
        EvidenceObserver().observe("org/repo", SHA, {"workflow_runs": [{"repository": "other/repo", "commit_sha": SHA, "conclusion": "success"}]})


def test_wrong_sha_rejected():
    with pytest.raises(ValueError, match="SHA"):
        EvidenceObserver().observe("org/repo", SHA, {"jobs": [{"repository": "org/repo", "commit_sha": "0" * 40, "conclusion": "success"}]})
