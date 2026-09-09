import json
from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_client_validation_policy_is_registry_owned_and_command_free():
    policy = json.loads(read("factory/registry/client-validation-policy.json"))
    assert policy["authority"] == "NIRA"
    assert policy["mode"] == "client-native-workflow-observation"
    assert set(policy["clients"]) == {
        "mobinpda-lab/Arvin-clean",
        "mobinpda-lab/YadNegar",
        "mobinpda-lab/NetworkCenterMonitor",
    }
    raw = json.dumps(policy)
    for forbidden in ("flutter test", "flutter analyze", "gradlew", "npm test", "pytest"):
        assert forbidden not in raw


def test_client_validation_contract_has_exact_head_and_no_promotion_authority():
    workflow = read(".github/workflows/nira-client-validation.yml")
    assert "EXPECTED_HEAD_SHA" in workflow
    assert "pr.data.head.sha !== expectedHead" in workflow
    assert "pr.data.base.ref !== 'main'" in workflow
    assert "FORK_HEAD_REJECTED" in workflow
    assert "listWorkflowRunsForRepo" in workflow
    assert "head_sha: expectedHead" in workflow
    assert "NIRA_CLIENT_VALIDATION_BLOCKED" in workflow
    assert "pulls.merge" not in workflow
    assert "merge_method" not in workflow
    assert "createOrUpdateFileContents" not in workflow


def test_worker_hands_client_pr_to_independent_validation():
    worker = read(".github/workflows/nira-cross-repo-worker.yml")
    assert "nira-client-validation.yml" in worker
    assert "NIRA_CLIENT_VALIDATION_DISPATCH=REQUESTED" in worker
    assert "steps.execute.outputs.pr_number" in worker
    assert "steps.execute.outputs.commit_sha" in worker
    assert "inputs.repository != 'mobinpda-lab/NIRA'" in worker


def test_registry_no_longer_claims_nira_ci_for_product_clients():
    registry = read("factory/registry/projects.example.yaml")
    policy = read("factory/registry/client-validation-policy.json")
    assert registry.count("validation_policy: factory/registry/client-validation-policy.json") == 3
    assert "Arvin Parallel Wave" in registry
    assert "YadNegar CI" in registry
    assert "Android Security" in registry
    assert '"Arvin Parallel Wave"' in policy
    assert '"YadNegar CI"' in policy
    assert '"Android CI"' in policy
