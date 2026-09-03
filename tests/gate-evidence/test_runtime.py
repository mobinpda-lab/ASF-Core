import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

models = load(ROOT / "gate-evidence/collector/models.py")
evaluator = load(ROOT / "gate-evidence/evaluator/gate_evaluator.py")
matrix = load(ROOT / "gate-evidence/evaluator/gate_matrix.py")
store = load(ROOT / "gate-evidence/evidence-store/store.py")
orchestrator = load(ROOT / "gate-evidence/orchestrator_boundary.py")

SHA = "a" * 40

def ev(state, sha=SHA, branch="main"):
    return models.GateEvidence("repo", sha, workflow="ci", event="pull_request", run_id=1, timestamp="2026-09-04T00:00:00+03:30", status=models.EvidenceStatus(state), branch=branch)

def test_all_success_allows():
    assert evaluator.evaluate([ev("SUCCESS")]) == evaluator.PromotionDecision.ALLOW

def test_fail_closed_states():
    for state in ("FAILURE", "PENDING", "NOT_FOUND", "NOT_EXPOSED"):
        assert evaluator.evaluate([ev(state)]) == evaluator.PromotionDecision.BLOCK

def test_empty_blocks():
    assert evaluator.evaluate([]) == evaluator.PromotionDecision.BLOCK

def test_stale_sha_blocks_matrix():
    result = matrix.evaluate_matrix("repo", SHA, [ev("SUCCESS", "b" * 40)])
    assert result.decision == matrix.PromotionDecision.BLOCK

def test_wrong_branch_blocks_matrix():
    result = matrix.evaluate_matrix("repo", SHA, [ev("SUCCESS", branch="feature/x")], expected_branch="main")
    assert result.decision == matrix.PromotionDecision.BLOCK

def test_duplicate_evidence_rejected():
    s = store.EvidenceStore(); record = ev("SUCCESS"); s.append("x", record)
    try: s.append("x", record)
    except ValueError: return
    assert False

def test_orchestrator_consumes_fail_closed_matrix():
    assert orchestrator.promotion_decision("repo", SHA, [ev("NOT_EXPOSED")]) == orchestrator.PromotionDecision.BLOCK

def test_normalized_output_is_machine_readable():
    out = ev("SUCCESS").normalized()
    assert out["commit_sha"] == SHA
    assert out["workflow"] == "ci"
    assert out["event"] == "pull_request"
    assert out["run_id"] == 1
    assert out["decision"] == "SUCCESS"
