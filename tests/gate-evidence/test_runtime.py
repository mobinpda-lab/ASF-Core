import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(p):
 s=importlib.util.spec_from_file_location(p.stem,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
c=load(ROOT/'gate-evidence/collector/models.py'); e=load(ROOT/'gate-evidence/evaluator/gate_evaluator.py'); st=load(ROOT/'gate-evidence/evidence-store/store.py')
def ev(status,sha='a'*40): return c.GateEvidence('repo',sha,status=c.EvidenceStatus(status),timestamp='2026-09-04T00:00:00+03:30')
def test_success(): assert e.evaluate([ev('SUCCESS')])==e.PromotionDecision.ALLOW
def test_all_blocking_states():
 for x in ('FAILURE','PENDING','NOT_FOUND','NOT_EXPOSED'): assert e.evaluate([ev(x)])==e.PromotionDecision.BLOCK
def test_empty_blocks(): assert e.evaluate([])==e.PromotionDecision.BLOCK
def test_stale_sha_filtered():
 from gate_evidence.correlator.correlation import correlate
 assert len(correlate([ev('SUCCESS','a'*40),ev('SUCCESS','b'*40)],'repo','a'*40))==1
def test_duplicate_rejected():
 s=st.EvidenceStore(); r=ev('SUCCESS'); s.append('x',r)
 try: s.append('x',r)
 except ValueError: return
 assert False
