import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path: str):
    return json.loads(read(path))


def test_autonomous_self_completion_runs_every_five_minutes_without_main_write():
    workflow = read(".github/workflows/nira-autonomous-self-completion.yml")
    assert "cron: '*/5 * * * *'" in workflow
    assert "contents: read" in workflow
    assert "contents: write" not in workflow
    assert "pull-requests: write" in workflow
    assert "issues: write" in workflow
    assert "nira-intake-queue.yml" in workflow
    assert "nira-queue-scheduler.yml" in workflow
    assert "createOrUpdateFileContents" not in workflow
    assert "NIRA Production Orchestrator" in workflow


def test_self_completion_plan_is_bounded_and_uses_existing_surfaces():
    plan = read_json("factory/registry/self-completion-plan.json")
    assert plan["repository"] == "mobinpda-lab/NIRA"
    assert len(plan["tasks"]) >= 5
    ids = {task["id"] for task in plan["tasks"]}
    assert len(ids) == len(plan["tasks"])
    for task in plan["tasks"]:
        assert 1 <= len(task["allowed_paths"]) <= 8
        assert set(task.get("depends_on", [])) <= ids
        for path in task["allowed_paths"]:
            assert (ROOT / path).is_file(), path
            assert not path.startswith(".github/workflows/")
            assert "secret" not in path.lower()
            assert "credential" not in path.lower()
            assert "token" not in path.lower()


def test_autonomous_mutation_policy_is_pr_only_and_protects_core_authorities():
    policy = read_json("factory/registry/autonomous-mutation-policy.json")
    assert policy["direct_main_writes_allowed"] is False
    assert policy["mutation_boundary"]["mode"] == "PR_ONLY"
    assert policy["mutation_boundary"]["required_branch_prefix"] == "nira/"
    assert policy["mutation_boundary"]["required_promotion_label"] == "nira-authorized"
    protected = set(policy["protected_paths"])
    for path in (
        ".github/workflows/production-orchestrator.yml",
        ".github/workflows/nira-queue-scheduler.yml",
        ".github/workflows/nira-lease.yml",
        ".github/workflows/nira-cross-repo-worker.yml",
        "factory/registry/promotion-policy.json",
        "factory/registry/autonomous-mutation-policy.json",
        "factory/registry/self-completion-plan.json",
    ):
        assert path in protected


def test_self_completion_requires_exact_main_factory_gates():
    plan = read_json("factory/registry/self-completion-plan.json")
    policy = read_json("factory/registry/autonomous-mutation-policy.json")
    expected = {
        "NIRA CI",
        "NIRA Factory E2E",
        "NIRA Factory Conformance",
        "NIRA Security Gate",
    }
    assert set(plan["required_workflows"]) == expected
    assert set(policy["required_exact_main_workflows"]) == expected
    workflow = read(".github/workflows/nira-autonomous-self-completion.yml")
    assert "head_sha === mainSha" in workflow
    assert "conclusion === 'success'" in workflow
    assert "NIRA_V1_SELF_COMPLETION=CERTIFIED" in workflow


def test_self_completion_scope_guard_authorizes_but_does_not_merge():
    workflow = read(".github/workflows/nira-autonomous-self-completion.yml")
    assert "listFiles" in workflow
    assert "task.allowed_paths" in workflow
    assert "policy.protected_paths" in workflow
    assert "do-not-merge" in workflow
    assert "nira-authorized" in workflow
    assert "NIRA_SELF_COMPLETION_SCOPE=AUTHORIZED" in workflow
    assert "github.rest.pulls.merge" not in workflow
    assert "merge_pull_request" not in workflow


def test_self_completion_closes_stale_base_and_requeues_instead_of_force_updating():
    workflow = read(".github/workflows/nira-autonomous-self-completion.yml")
    assert "STALE_BASE_REQUEUE" in workflow
    assert "pr.base?.sha !== mainSha" in workflow
    assert "state: 'closed'" in workflow
    assert "factory:ready" in workflow
    assert "force" not in workflow.lower()


def test_completion_gate_documents_chat_independence_and_fail_closed_rules():
    gate = read("docs/NIRA_COMPLETION_GATE.md")
    assert "without requiring a user to type `continue`" in gate
    assert "GitHub Issues" in gate
    assert "Fail-closed rules" in gate
    assert "NIRA_V1_SELF_COMPLETION=CERTIFIED" in gate
    assert "does not write directly to `main`" in gate
