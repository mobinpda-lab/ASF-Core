from dataclasses import dataclass

@dataclass(frozen=True)
class CorrelationKey:
    repository: str
    commit_sha: str
    workflow: str = ""
    event: str = ""
    run_id: int = 0
    job_id: int = 0
    artifact_id: int = 0
    check_id: int = 0

def correlate(evidence, repository, commit_sha, workflow=None, event=None, run_id=None, job_id=None, artifact_id=None, check_id=None):
    result = []
    for item in evidence:
        if getattr(item, "repository", None) != repository or getattr(item, "commit_sha", None) != commit_sha: continue
        if workflow is not None and getattr(item, "workflow", None) != workflow: continue
        if event is not None and getattr(item, "event", None) != event: continue
        if run_id is not None and getattr(item, "run_id", None) != run_id: continue
        if job_id is not None and getattr(item, "job_id", None) != job_id: continue
        if artifact_id is not None and getattr(item, "artifact_id", None) != artifact_id: continue
        if check_id is not None and getattr(item, "check_id", None) != check_id: continue
        result.append(item)
    return result

def branch_matches(actual_branch, expected_branch): return actual_branch == expected_branch
