import unittest

from core.evidence import EvidenceObserver, GitHubAdapter, ObservationState, Visibility


SHA = "a" * 40
REPO = "mobinpda-lab/ASF-Core"


def source(**overrides):
    value = {
        "workflow_runs": [{"repository": REPO, "commit_sha": SHA, "conclusion": "success"}],
        "check_runs": [{"repository": REPO, "commit_sha": SHA, "conclusion": "success"}],
        "jobs": [{"repository": REPO, "commit_sha": SHA, "conclusion": "success"}],
        "artifacts": [{"repository": REPO, "commit_sha": SHA, "id": 1}],
        "statuses": [{"repository": REPO, "commit_sha": SHA, "state": "success"}],
    }
    value.update(overrides)
    return value


class ProviderAdapterHardeningTests(unittest.TestCase):
    def test_provider_available(self):
        result = GitHubAdapter().observe(REPO, SHA, source())
        self.assertEqual(result.observation, ObservationState.AVAILABLE)
        self.assertEqual(result.confidence, "HIGH")

    def test_provider_unavailable(self):
        result = GitHubAdapter().observe(REPO, SHA, {"accessible": False})
        self.assertEqual(result.observation, ObservationState.UNAVAILABLE)
        self.assertEqual(result.confidence, "LOW")

    def test_partial_response(self):
        data = source(); del data["statuses"]
        result = GitHubAdapter().observe(REPO, SHA, data)
        self.assertEqual(result.observation, ObservationState.PARTIAL)

    def test_delayed_response(self):
        result = GitHubAdapter().observe(REPO, SHA, source(delayed=True, retry_after=5))
        self.assertEqual(result.observation, ObservationState.DELAYED)

    def test_inconsistent_response(self):
        result = GitHubAdapter().observe(REPO, SHA, source(inconsistent=True))
        self.assertEqual(result.observation, ObservationState.INCONSISTENT)

    def test_false_success_prevention(self):
        observer = EvidenceObserver()
        result = observer.observe_provider(REPO, SHA, GitHubAdapter().observe(REPO, SHA, {"accessible": False}))
        self.assertNotEqual(result.state, Visibility.SUCCESS)

    def test_exact_sha_mismatch(self):
        with self.assertRaises(ValueError):
            GitHubAdapter().observe(REPO, SHA, source(workflow_runs=[{"repository": REPO, "commit_sha": "b" * 40, "conclusion": "success"}]))

    def test_wrong_repository_rejection(self):
        with self.assertRaises(ValueError):
            GitHubAdapter().observe(REPO, SHA, source(check_runs=[{"repository": "other/repo", "commit_sha": SHA, "conclusion": "success"}]))


if __name__ == "__main__":
    unittest.main()
