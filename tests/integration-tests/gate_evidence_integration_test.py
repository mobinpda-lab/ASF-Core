import importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path); module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
models = load(ROOT / "gate-evidence/collector/models.py")
collectors = load(ROOT / "gate-evidence/collector/github_collectors.py")
correlator = load(ROOT / "gate-evidence/correlator/correlation.py")
SHA = "a" * 40

def test_workflow_collector_normalizes_success_and_identity():
    c = collectors.WorkflowRunCollector(lambda **_: {"workflow_runs": [{"id": 42, "name": "validation", "event": "pull_request", "head_branch": "main", "conclusion": "success", "updated_at": "2026-09-04T00:00:00+03:30"}]})
    result = c.collect("repo", SHA)[0]
    assert result.status == models.EvidenceStatus.SUCCESS
    assert result.run_id == 42 and result.workflow == "validation" and result.event == "pull_request"

def test_hidden_evidence_is_not_exposed():
    c = collectors.WorkflowRunCollector(lambda **_: {"workflow_runs": [{"not_exposed": True}]})
    assert c.collect("repo", SHA)[0].status == models.EvidenceStatus.NOT_EXPOSED

def test_missing_evidence_is_not_found():
    c = collectors.WorkflowRunCollector(lambda **_: None)
    assert c.collect("repo", SHA)[0].status == models.EvidenceStatus.NOT_FOUND

def test_correlation_rejects_stale_sha_and_accepts_exact_sha():
    exact = models.GateEvidence("repo", SHA, workflow="validation", event="pull_request", run_id=42)
    stale = models.GateEvidence("repo", "b" * 40, workflow="validation", event="pull_request", run_id=43)
    assert correlator.correlate([exact, stale], "repo", SHA) == [exact]
    assert correlator.correlate([exact], "repo", "b" * 40) == []

def test_identifier_correlation_can_narrow_run():
    exact = models.GateEvidence("repo", SHA, workflow="validation", event="pull_request", run_id=42)
    other = models.GateEvidence("repo", SHA, workflow="validation", event="push", run_id=43)
    assert correlator.correlate([exact, other], "repo", SHA, workflow="validation", event="pull_request", run_id=42) == [exact]
