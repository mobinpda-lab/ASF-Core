import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load(path):
    spec=importlib.util.spec_from_file_location(path.stem, path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

collector=load(ROOT/'gate-evidence/collector/models.py')
evaluator=load(ROOT/'gate-evidence/evaluator/gate_evaluator.py')
store=load(ROOT/'gate-evidence/evidence-store/store.py')

def ev(status, sha='a'*40):
    return collector.GateEvidence('repo', sha, status=collector.EvidenceStatus(status), timestamp='2026-09-04T00:00:00+03:30')

def test_all_success(): assert evaluator.evaluate([ev('SUCCESS'),ev('SUCCESS')]) == evaluator.PromotionDecision.ALLOW

def test_unresolved_states_block():
    for status in ('FAILURE','PENDING','NOT_FOUND','NOT_EXPOSED'):
        assert evaluator.evaluate([ev(status)]) == evaluator.PromotionDecision.BLOCK

def test_empty_blocks(): assert evaluator.evaluate([]) == evaluator.PromotionDecision.BLOCK

def test_stale_sha_excluded():
    from gate_evidence.correlator.correlation import correlate
    assert len(correlate([ev('SUCCESS','a'*40),ev('SUCCESS','b'*40)],'repo','a'*40)) == 1

def test_duplicate_evidence_rejected():
    s=store.EvidenceStore(); r=ev('SUCCESS'); s.append('e1',r)
    try: s.append('e1',r)
    except ValueError: return
    assert False
