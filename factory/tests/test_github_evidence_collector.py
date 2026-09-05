from __future__ import annotations

from factory.contracts.schema import ObservationState
from factory.evidence.github_collector import EvidenceRequirements, collect_pr_evidence


class FakeGitHub:
    def pull_request(self, repo, number):
        return {
            "state": "open",
            "base": {"sha": "b" * 40},
            "head": {"sha": "h" * 40},
        }

    def commit_status(self, repo, sha):
        return {"statuses": [{"context": "ci", "state": "success"}]}

    def check_runs(self, repo, sha):
        return {"check_runs": [{"name": "ASF-Core CI", "status": "completed", "conclusion": "success"}]}

    def workflow_runs_for_head(self, repo, sha):
        return {
            "workflow_runs": [
                {
                    "id": 123,
                    "workflow_id": 77,
                    "name": "ASF-Core CI",
                    "status": "completed",
                    "conclusion": "success",
                    "head_sha": sha,
                },
                {
                    "id": 124,
                    "workflow_id": 78,
                    "name": "NIRA Security Gate",
                    "status": "completed",
                    "conclusion": "success",
                    "head_sha": sha,
                },
            ]
        }

    def workflow_run_artifacts(self, repo, run_id):
        return {"artifacts": [{"id": 1, "name": "evidence", "digest": "sha256:test"}]}


def test_collector_derives_verified_state_from_github_observations():
    evidence = collect_pr_evidence(
        FakeGitHub(),
        repo="mobinpda-lab/Arvin-clean",
        project_id="arvin-clean",
        task_id="task-1",
        pr_number=659,
        expected_base_sha="b" * 40,
        expected_head_sha="h" * 40,
        requirements=EvidenceRequirements(
            required_workflows=("ASF-Core CI",),
            require_commit_status=True,
            require_artifact=True,
            require_security=True,
        ),
    )
    assert evidence.observation_state is ObservationState.VERIFIED
    assert evidence.confidence == "HIGH"
    assert evidence.artifact_digests == ("sha256:test",)


def test_collector_fails_closed_when_security_is_missing():
    fake = FakeGitHub()
    fake.workflow_runs_for_head = lambda repo, sha: {
        "workflow_runs": [
            {
                "id": 123,
                "workflow_id": 77,
                "name": "ASF-Core CI",
                "status": "completed",
                "conclusion": "success",
                "head_sha": sha,
            }
        ]
    }
    evidence = collect_pr_evidence(
        fake,
        repo="mobinpda-lab/Arvin-clean",
        project_id="arvin-clean",
        task_id="task-2",
        pr_number=659,
        expected_base_sha="b" * 40,
        expected_head_sha="h" * 40,
        requirements=EvidenceRequirements(required_workflows=("ASF-Core CI",), require_security=True),
    )
    assert evidence.observation_state is ObservationState.NOT_EXPOSED
    assert evidence.confidence == "NONE"
