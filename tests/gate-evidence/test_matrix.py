import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(path):
 s=importlib.util.spec_from_file_location(path.stem,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
c=load(ROOT/'gate-evidence/collector/models.py'); e=load(ROOT/'gate-evidence/evaluator/gate_matrix.py')
def ev(status): return c.GateEvidence('repo','a'*40,status=c.EvidenceStatus(status),timestamp='2026-09-04T00:00:00+03:30')
def test_matrix_allow(): assert e.evaluate_matrix('repo','a'*40,[ev('SUCCESS')]).decision == e.PromotionDecision.ALLOW
def test_matrix_fail_closed(): assert e.evaluate_matrix('repo','a'*40,[ev('SUCCESS'),ev('PENDING')]).decision == e.PromotionDecision.BLOCK
