import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_schema_json():
 for p in [ROOT/'schemas/gate-state/gate-state.schema.json',ROOT/'schemas/evidence-record/evidence-record.schema.json',ROOT/'schemas/promotion-decision/promotion-decision.schema.json']:json.loads(p.read_text())
def test_runtime_files():
 for p in [ROOT/'gate-evidence/collector/models.py',ROOT/'gate-evidence/collector/github_collectors.py',ROOT/'gate-evidence/correlator/correlation.py',ROOT/'gate-evidence/evaluator/gate_evaluator.py',ROOT/'gate-evidence/evaluator/gate_matrix.py',ROOT/'gate-evidence/evidence-store/store.py',ROOT/'gate-evidence/orchestrator_boundary.py']:assert p.is_file()
