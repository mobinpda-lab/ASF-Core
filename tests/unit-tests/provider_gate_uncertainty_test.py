import unittest

from core.evidence import EvidenceRecord, ObservationState, Visibility, promotion_matrix


class ProviderGateUncertaintyTests(unittest.TestCase):
    def test_provider_uncertainty_cannot_allow_success(self):
        record = EvidenceRecord("repo", "a" * 40, (), (), (), (), (), Visibility.SUCCESS,
                                ObservationState.PARTIAL, "LOW", "missing statuses")
        gate = promotion_matrix(record)[0]
        self.assertEqual(gate.decision, "BLOCK")
        self.assertEqual(gate.confidence, "LOW")

    def test_available_success_can_allow(self):
        record = EvidenceRecord("repo", "a" * 40, ({"conclusion": "success"},), (), (), (), (), Visibility.SUCCESS,
                                ObservationState.AVAILABLE, "HIGH", "all sections observable")
        gate = promotion_matrix(record)[0]
        self.assertEqual(gate.decision, "ALLOW")
        self.assertEqual(gate.confidence, "HIGH")


if __name__ == "__main__":
    unittest.main()
