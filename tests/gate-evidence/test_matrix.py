import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(p):
 s=importlib.util.spec_from_file_location(p.stem,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
c=load(ROOT/'gate-evidence/collector/models.py'); m=load(ROOT/'gate-evidence/evaluator/gate_matrix.py')
def ev(x,branch=None): return c.GateEvidence('repo','a'*40,status=c.EvidenceStatus(x),branch=branch,timestamp='2026-09-04T00:00:00+03:30')
def test_allow(): assert m.evaluate_matrix('repo','a'*40,[ev('SUCCESS')]).decision==m.PromotionDecision.ALLOW
def test_block_pending(): assert m.evaluate_matrix('repo','a'*40,[ev('SUCCESS'),ev('PENDING')]).decision==m.PromotionDecision.BLOCK
def test_wrong_branch_blocks(): assert m.evaluate_matrix('repo','a'*40,[ev('SUCCESS','main')],expected_branch='feature').decision==m.PromotionDecision.BLOCK
