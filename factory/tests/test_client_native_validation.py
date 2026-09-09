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


def test_client_promotion_is_separate_exact_head_authority():
    promotion = read(".github/workflows/nira-client-promotion.yml")
    assert "NIRA_CLIENT_PROMOTION=UNREGISTERED_CLIENT" in promotion
    assert "HEAD_NAMESPACE_REJECTED" in promotion
    assert "LEASE_PROVENANCE_NOT_OBSERVED" in promotion
    assert "BASE_DRIFT" in promotion
    assert "GATE_NOT_VERIFIED" in promotion
    assert "MAIN_MOVED_DURING_VALIDATION" in promotion
    assert "sha: expectedHead" in promotion
    assert "POSTCONDITION_MAIN_MISMATCH" in promotion
    assert "factory:completed" in promotion
    assert "createOrUpdateFileContents" not in promotion


def test_validation_hands_only_verified_head_to_promotion():
    validation = read(".github/workflows/nira-client-validation.yml")
    assert "Hand verified client head to separate promotion authority" in validation
    assert "if: success()" in validation
    assert "nira-client-promotion.yml" in validation
    assert "expected_head_sha" in validation
    assert "control_issue_number" in validation


def test_client_promotion_persists_truth_independent_of_optional_issue_metadata():
    promotion = read(".github/workflows/nira-client-promotion.yml")
    assert "nira-client-promotion-evidence.json" in promotion
    assert "observation_state: 'VERIFIED'" in promotion
    assert "confidence: 'HIGH'" in promotion
    assert "Completion comment failed after verified merge" in promotion
    assert "Optional completion label unavailable" in promotion
    assert "Upload cross-repository promotion evidence" in promotion


def test_client_validation_is_read_only_by_default_and_worker_opts_into_promotion():
    validation = read(".github/workflows/nira-client-validation.yml")
    worker = read(".github/workflows/nira-cross-repo-worker.yml")
    assert "default: false" in validation
    assert "inputs.promote == true" in validation
    assert "promote: 'true'" in worker
