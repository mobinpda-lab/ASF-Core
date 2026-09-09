import json
from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_release_policy_is_client_native_and_explicitly_disables_unproven_client():
    policy = json.loads(read("factory/registry/client-release-policy.json"))
    assert policy["authority"] == "NIRA"
    assert policy["mode"] == "client-native-release-orchestration"
    assert policy["clients"]["mobinpda-lab/Arvin-clean"]["enabled"] is True
    assert policy["clients"]["mobinpda-lab/YadNegar"]["enabled"] is True
    assert policy["clients"]["mobinpda-lab/NetworkCenterMonitor"]["enabled"] is False
    raw = json.dumps(policy).lower()
    for command in ("flutter build", "./gradlew", "npm run", "pytest"):
        assert command not in raw


def test_release_worker_observes_exact_main_and_never_merges_or_builds_product():
    wf = read(".github/workflows/nira-client-release.yml")
    assert "EXPECTED_MAIN_SHA" in wf
    assert "MAIN_DRIFT" in wf
    assert "NO_GITHUB_RELEASE_FOR_EXACT_MAIN" in wf
    assert "nira-client-release-evidence.json" in wf
    assert "observation_state: 'VERIFIED'" in wf
    assert "pulls.merge" not in wf
    assert "createOrUpdateFileContents" not in wf
    assert "flutter build" not in wf
    assert "./gradlew" not in wf


def test_client_promotion_dispatches_release_only_after_verified_merge_and_policy_opt_in():
    wf = read(".github/workflows/nira-client-promotion.yml")
    assert "id: promote" in wf
    assert "release_enabled" in wf
    assert "nira-client-release.yml" in wf
    assert "steps.promote.outputs.release_enabled == 'true'" in wf
    assert "steps.promote.outputs.promoted_main_sha" in wf


def test_monitor_only_reconciles_issues_and_never_auto_queues_repair():
    wf = read(".github/workflows/nira-client-monitor.yml")
    assert "NIRA Client Monitor" in wf
    assert "CLIENT_REPOSITORY: " in wf
    assert "FAILED_WORKFLOW: " in wf
    assert "NIRA_WORKER_ROLE: RECOVERY" in wf
    assert "NIRA_MONITOR_RECOVERY=VERIFIED" in wf
    assert "factory:ready" not in wf
    assert "nira-cross-repo-worker.yml" not in wf
    assert "pulls.merge" not in wf
    assert "createOrUpdateFileContents" not in wf


def test_project_registry_release_contract_matches_release_policy():
    registry = read("factory/registry/projects.example.yaml")
    assert registry.count("policy: factory/registry/client-release-policy.json") == 2
    assert "no_registered_client_release_workflow" in registry
    assert "release_verified" in registry
