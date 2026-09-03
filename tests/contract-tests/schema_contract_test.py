import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[2]
SCHEMAS = [
    ROOT / 'schemas/task-state/task-lifecycle.schema.json',
    ROOT / 'schemas/task-state/worker-state.schema.json',
    ROOT / 'schemas/lifecycle/queue-state.schema.json',
    ROOT / 'schemas/lifecycle/recovery-state.schema.json',
    ROOT / 'schemas/evidence/evidence-record.schema.json',
    ROOT / 'schemas/release-state/release-state.schema.json',
]

class SchemaContractTests(unittest.TestCase):
    def test_schema_files_are_valid_json(self):
        for path in SCHEMAS:
            with self.subTest(path=str(path)):
                data = json.loads(path.read_text())
                self.assertEqual(data.get('$schema'), 'https://json-schema.org/draft/2020-12/schema')
                self.assertEqual(data.get('type'), 'object')
                self.assertTrue(data.get('required'))

    def test_expected_state_enums_exist(self):
        expected = {
            'task-lifecycle.schema.json': 'completed',
            'worker-state.schema.json': 'running',
            'queue-state.schema.json': 'leased',
            'recovery-state.schema.json': 'resumable',
            'release-state.schema.json': 'released',
        }
        for name, state in expected.items():
            matches = [p for p in SCHEMAS if p.name == name]
            self.assertEqual(len(matches), 1)
            text = matches[0].read_text()
            self.assertIn(state, text)

if __name__ == '__main__':
    unittest.main()
