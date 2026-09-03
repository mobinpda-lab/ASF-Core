from typing import Any, Callable, Iterable
try:
    from .models import EvidenceStatus, GateEvidence, status_from_conclusion
except ImportError:
    import importlib.util
    from pathlib import Path
    _spec = importlib.util.spec_from_file_location("gate_evidence_models", Path(__file__).with_name("models.py"))
    _models = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_models)
    EvidenceStatus, GateEvidence, status_from_conclusion = _models.EvidenceStatus, _models.GateEvidence, _models.status_from_conclusion

def _items(raw: Any) -> list:
    if raw is None: return []
    if isinstance(raw, dict): return raw.get("workflow_runs") or raw.get("check_runs") or raw.get("jobs") or raw.get("artifacts") or [raw]
    return list(raw) if isinstance(raw, Iterable) and not isinstance(raw, (str, bytes)) else [raw]

def normalize_run(repository: str, commit_sha: str, raw: Any, source: str = "github") -> GateEvidence:
    if raw is None: return GateEvidence(repository, commit_sha, status=EvidenceStatus.NOT_FOUND, evidence_source=source)
    if isinstance(raw, dict) and raw.get("not_exposed"): return GateEvidence(repository, commit_sha, status=EvidenceStatus.NOT_EXPOSED, evidence_source=source)
    data = raw if isinstance(raw, dict) else {}
    conclusion = data.get("conclusion")
    return GateEvidence(repository, commit_sha, workflow=data.get("name") or data.get("workflow"), event=data.get("event"), run_id=data.get("id") or data.get("run_id"), job_id=data.get("job_id"), artifact_id=data.get("artifact_id"), check_id=data.get("check_id") or data.get("check_run_id"), conclusion=conclusion, timestamp=data.get("updated_at") or data.get("created_at") or "", branch=data.get("head_branch") or data.get("branch"), status=status_from_conclusion(conclusion), evidence_source=source)

class WorkflowRunCollector:
    def __init__(self, fetch: Callable[..., Any]): self.fetch = fetch
    def collect(self, repository, commit_sha):
        raw = self.fetch(repository=repository, commit_sha=commit_sha); return [normalize_run(repository, commit_sha, item) for item in _items(raw)] or [normalize_run(repository, commit_sha, None)]
class CheckRunCollector:
    def __init__(self, fetch: Callable[..., Any]): self.fetch = fetch
    def collect(self, repository, commit_sha):
        raw = self.fetch(repository=repository, commit_sha=commit_sha); return [normalize_run(repository, commit_sha, item, "github-check") for item in _items(raw)] or [normalize_run(repository, commit_sha, None, "github-check")]
class JobResultCollector:
    def __init__(self, fetch: Callable[..., Any]): self.fetch = fetch
    def collect(self, repository, run_id): return self.fetch(repository=repository, run_id=run_id)
class ArtifactResultCollector:
    def __init__(self, fetch: Callable[..., Any]): self.fetch = fetch
    def collect(self, repository, run_id): return self.fetch(repository=repository, run_id=run_id)
