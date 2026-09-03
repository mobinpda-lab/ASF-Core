import importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path); module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
m = load(ROOT / "gate-evidence/collector/models.py")
e = load(ROOT / "gate-evidence/evaluator/gate_evaluator.py")
x = load(ROOT / "gate-evidence/evaluator/gate_matrix.py")
s = load(ROOT / "gate-evidence/evidence-store/store.py")
o = load(ROOT / "gate-evidence/orchestrator_boundary.py")
SHA = "a" * 40
def ev(state, sha=SHA, branch="main"):
    return m.GateEvidence("repo", sha, workflow="ci", event="pull_request", run_id=1, timestamp="2026-09-04T00:00:00+03:30", status=m.EvidenceStatus(state), branch=branch)
def test_all_success_allows(): assert e.evaluate([ev("SUCCESS")]) == e.PromotionDecision.ALLOW
def test_fail_closed_states():
    for state in ("FAILURE", "PENDING", "NOT_FOUND", "NOT_EXPOSED"): assert e.evaluate([ev(state)]) == e.PromotionDecision.BLOCK
def test_stale_sha_blocks(): assert x.evaluate_matrix("repo", SHA, [ev("SUCCESS", "b" * 40)]).decision == x.PromotionDecision.BLOCK
def test_wrong_branch_blocks(): assert x.evaluate_matrix("repo", SHA, [ev("SUCCESS", branch="feature")], "main").decision == x.PromotionDecision.BLOCK
def test_duplicate_rejected():
    store = s.EvidenceStore(); record = ev("SUCCESS"); store.append("id", record)
    try: store.append("id", record)
    except ValueError: return
    assert False
def test_not_exposed_blocks_orchestrator(): assert o.promotion_decision("repo", SHA, [ev("NOT_EXPOSED")]) == o.PromotionDecision.BLOCK
def test_normalized_output():
    data = ev("SUCCESS").normalized(); assert data["commit_sha"] == SHA and data["workflow"] == "ci" and data["decision"] == "SUCCESS"
