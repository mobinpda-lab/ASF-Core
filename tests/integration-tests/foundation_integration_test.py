import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[2]

class FoundationIntegrationTests(unittest.TestCase):
    def test_foundation_surfaces_are_connected(self):
        self.assertTrue((ROOT / 'docs/ASF-MOC-v9.md').is_file())
        self.assertTrue((ROOT / 'docs/architecture/ARCHITECTURE.md').is_file())
        self.assertTrue((ROOT / 'docs/governance/GOVERNANCE.md').is_file())
        self.assertTrue((ROOT / '.github/workflows/validation.yml').is_file())

    def test_schema_and_contract_policy_are_machine_readable(self):
        evidence = json.loads((ROOT / 'schemas/evidence/evidence-record.schema.json').read_text())
        self.assertIn('commit_sha', evidence['required'])
        self.assertEqual(evidence['properties']['commit_sha']['pattern'], '^[0-9a-fA-F]{40}$')
        governance = (ROOT / 'docs/governance/GOVERNANCE.md').read_text()
        self.assertIn('Production Orchestrator', governance)
        self.assertIn('must not write directly to `main`', governance)

if __name__ == '__main__':
    unittest.main()
