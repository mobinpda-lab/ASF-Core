import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(path):
 s=importlib.util.spec_from_file_location(path.stem,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
c=load(ROOT/'gate-evidence/collector/models.py'); e=load(ROOT/'gate-evidence/evaluator/gate_evaluator.py'); st=load(ROOT/'gate-evidence/evidence-store/store.py')
def ev(status,sha='a'*40): return c.GateEvidence('repo',sha,status=c.EvidenceStatus(status),timestamp='2026-09-04T00:00:00+03:30')
def test_all_success(): assert e.evaluate([ev('SUCCESS'),ev('SUCCESS')]) == e.PromotionDecision.ALLOW
def test_unresolved_states_block():
 for x in ('FAILURE','PENDING','NOT_FOUND','NOT_EXPOSED'): assert e.evaluate([ev(x)]) == e.PromotionDecision.BLOCK
def test_empty_blocks(): assert e.evaluate([]) == e.PromotionDecision.BLOCK
def test_stale_sha_excluded():
 from gate_evidence.correlator.correlation import correlate
 assert len(correlate([ev('SUCCESS','a'*40),ev('SUCCESS','b'*40)],'repo','a'*40)) == 1
def test_duplicate_evidence_rejected():
 s=st.EvidenceStore(); r=ev('SUCCESS'); s.append('e1',r)
 try: s.append('e1',r)
 except ValueError: return
 assert False
