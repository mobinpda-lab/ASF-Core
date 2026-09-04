from core.evidence.ci_observer import EvidenceObserver

SHA = "6a26f23572a951642b4dea3b17d6a8f672b56e1f"


def test_timestamps_are_preserved_in_normalized_source():
    timestamp = "2026-09-04T00:00:00Z"
    source = {"workflow_runs": [{"commit_sha": SHA, "conclusion": "success", "created_at": timestamp}], "statuses": [{"commit_sha": SHA, "state": "success", "created_at": timestamp}]}
    record = EvidenceObserver().observe("org/repo", SHA, source)
    assert record.workflow_runs[0]["created_at"] == timestamp
    assert record.statuses[0]["created_at"] == timestamp
