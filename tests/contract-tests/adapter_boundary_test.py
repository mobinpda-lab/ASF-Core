import unittest
from pathlib import Path

ROOT = Path(__file__).parents[2]

class AdapterBoundaryTests(unittest.TestCase):
    def test_required_contracts_exist(self):
        contracts = [
            'core/orchestrator/CONTRACT.md',
            'core/queue/CONTRACT.md',
            'core/workers/CONTRACT.md',
            'core/evidence/CONTRACT.md',
            'core/state/CONTRACT.md',
            'adapters/PRODUCT_ADAPTER_CONTRACT.md',
        ]
        for rel in contracts:
            with self.subTest(path=rel):
                self.assertTrue((ROOT / rel).is_file())
                self.assertGreater((ROOT / rel).stat().st_size, 0)

    def test_adapter_contract_declares_boundary_controls(self):
        text = (ROOT / 'adapters/PRODUCT_ADAPTER_CONTRACT.md').read_text()
        for term in ('intake', 'state', 'validation', 'Isolation', 'least privilege'):
            self.assertIn(term, text)

    def test_product_repositories_are_not_embedded(self):
        text = (ROOT / 'adapters/PRODUCT_ADAPTER_CONTRACT.md').read_text()
        self.assertIn('remain in product repositories', text)

if __name__ == '__main__':
    unittest.main()
