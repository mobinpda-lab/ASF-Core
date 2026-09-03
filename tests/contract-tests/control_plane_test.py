import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(path,name):
 s=importlib.util.spec_from_file_location(name,ROOT/path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
life=load('core/state/lifecycle.py','life'); dec=load('core/orchestrator/decisions.py','dec')

def test_lifecycle_transitions_and_history():
 x=life.Lifecycle(); x.transition('QUEUED','intake'); x.transition('RUNNING','leased'); x.transition('FAILED','execution failure'); x.transition('RECOVERING','retryable')
 assert x.state==life.LifecycleState.RECOVERING and len(x.history)==4

def test_terminal_state_is_immutable():
 x=life.Lifecycle('COMPLETED')
 try: x.transition('QUEUED','invalid')
 except ValueError: return
 assert False

def test_decision_model():
 assert dec.decide(evidence_complete=True)==dec.Decision.ALLOW
 assert dec.decide(evidence_complete=False)==dec.Decision.WAIT
 assert dec.decide(evidence_failed=True)==dec.Decision.BLOCK
 assert dec.decide(evidence_failed=True,recoverable=True)==dec.Decision.RECOVER
 assert dec.decide(evidence_complete=True,dependencies_ready=False)==dec.Decision.WAIT
