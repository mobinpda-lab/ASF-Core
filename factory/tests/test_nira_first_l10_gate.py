from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_l10_activation_defaults_to_nira_self_proof():
    workflow = read(".github/workflows/nira-l10-activation.yml")
    assert "default: mobinpda-lab/NIRA" in workflow
    assert "default: mobinpda-lab/Arvin-clean" not in workflow
    assert "NIRA_L10_PROOF_SCOPE=NIRA_SELF_ONLY" in workflow
    assert "NIRA_L10_SELF_WORKER_DISPATCH=REQUESTED" in workflow


def test_l10_activation_rejects_external_clients_fail_closed():
    workflow = read(".github/workflows/nira-l10-activation.yml")
    assert "NIRA_L10=CLIENT_BLOCKED_UNTIL_NIRA_SELF_CERTIFIED" in workflow
    assert "NIRA_L10=REJECTED_NON_NIRA_TARGET" in workflow
    assert "process.env.TARGET_REPOSITORY !== canonicalNira" in workflow
    assert "process.env.CLIENT_REPOSITORY !== canonicalNira" in workflow


def test_l10_self_proof_preserves_worker_and_evidence_boundaries():
    workflow = read(".github/workflows/nira-l10-activation.yml")
    assert "nira-cross-repo-worker.yml" in workflow
    assert "expected_main_sha" in workflow
    assert "lease_id" in workflow
    assert "fence_token" in workflow
    assert "actions/upload-artifact@v4" in workflow
    assert "pulls.merge" not in workflow
    assert "contents: write" not in workflow


def test_l10_runbook_explicitly_defers_external_clients():
    runbook = read("docs/operations/NIRA_L10_ACTIVATION_WAVE_171.md")
    assert "does not use Arvin or any other external product as the current proof target" in runbook
    assert "External clients such as Arvin remain deferred" in runbook
    assert "SC-01" in runbook and "SC-06" in runbook
