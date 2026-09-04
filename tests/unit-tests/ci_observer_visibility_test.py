from core.evidence.ci_observer import EvidenceObserver, Visibility

SHA = "6a26f23572a951642b4dea3b17d6a8f672b56e1f"


def test_all_visibility_states():
    observer = EvidenceObserver()
    assert observer.observe("org/repo", SHA, {"authoritative_not_found": True}).state is Visibility.NOT_FOUND
    assert observer.observe("org/repo", SHA, {"accessible": False}).state is Visibility.NOT_EXPOSED
    assert observer.observe("org/repo", SHA, {"workflow_runs": [{"commit_sha": SHA, "conclusion": "in_progress"}]}).state is Visibility.PENDING
    assert observer.observe("org/repo", SHA, {"workflow_runs": [{"commit_sha": SHA, "conclusion": "failure"}]}).state is Visibility.FAILURE
    assert observer.observe("org/repo", SHA, {"workflow_runs": [{"commit_sha": SHA, "conclusion": "success"}]}).state is Visibility.SUCCESS
