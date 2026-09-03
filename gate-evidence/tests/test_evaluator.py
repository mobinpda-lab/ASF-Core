import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "evaluator"))
from evaluator import EvidenceState, GateEvaluation, evaluate

SHA = "a" * 40


class GateEvaluatorContractTests(unittest.TestCase):
    def test_all_success_allows(self):
        result = evaluate(SHA, ["validation", "evidence"], [
            GateEvaluation("validation", SHA, EvidenceState.SUCCESS),
            GateEvaluation("evidence", SHA, EvidenceState.SUCCESS),
        ])
        self.assertEqual(result.decision, "ALLOW")

    def test_all_blocking_states_block(self):
        for state in EvidenceState:
            if state is EvidenceState.SUCCESS:
                continue
            result = evaluate(SHA, ["gate"], [GateEvaluation("gate", SHA, state)])
            self.assertEqual(result.decision, "BLOCK")

    def test_missing_gate_is_not_found_and_blocks(self):
        result = evaluate(SHA, ["required"], [])
        self.assertEqual(result.gates[0].state, EvidenceState.NOT_FOUND)
        self.assertEqual(result.decision, "BLOCK")

    def test_stale_sha_blocks(self):
        result = evaluate(SHA, ["gate"], [GateEvaluation("gate", "b" * 40, EvidenceState.SUCCESS)])
        self.assertEqual(result.decision, "BLOCK")


if __name__ == "__main__":
    unittest.main()
