import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("observability", ROOT / "gate-evidence/observability/observability.py")
obs = importlib.util.module_from_spec(spec); spec.loader.exec_module(obs)
SHA = "a" * 40

def make(state):
    return obs.FactoryObservation("repo", SHA, "validation", "validation", "pull_request", 10, None, ("success",), (), state, obs.ObservationConfidence.HIGH, "2026-09-04T00:00:00+03:30", "test")

def test_visible_success_allows():
    matrix = obs.build_promotion_matrix([make(obs.VisibilityState.WORKFLOW_VISIBLE)], "repo", SHA, ["validation"])
    assert matrix["decision"] == "ALLOW" and matrix["gates"][0]["status"] == "SUCCESS"

def test_hidden_workflow_blocks_and_explains():
    matrix = obs.build_promotion_matrix([make(obs.VisibilityState.WORKFLOW_NOT_VISIBLE)], "repo", SHA, ["validation"])
    assert matrix["decision"] == "BLOCK" and matrix["gates"][0]["status"] == "NOT_EXPOSED"
    assert "observable" in matrix["gates"][0]["reason"]

def test_missing_workflow_is_not_found():
    matrix = obs.build_promotion_matrix([], "repo", SHA, ["validation"])
    assert matrix["gates"][0]["status"] == "NOT_FOUND" and matrix["decision"] == "BLOCK"

def test_wrong_repository_does_not_match():
    matrix = obs.build_promotion_matrix([make(obs.VisibilityState.WORKFLOW_VISIBLE)], "other", SHA, ["validation"])
    assert matrix["gates"][0]["status"] == "NOT_FOUND" and matrix["decision"] == "BLOCK"

def test_stale_sha_does_not_match():
    matrix = obs.build_promotion_matrix([obs.FactoryObservation("repo", "b" * 40, "validation", visibility_state=obs.VisibilityState.WORKFLOW_VISIBLE)], "repo", SHA, ["validation"])
    assert matrix["gates"][0]["status"] == "NOT_FOUND" and matrix["decision"] == "BLOCK"

def test_incomplete_evidence_blocks():
    matrix = obs.build_promotion_matrix([make(obs.VisibilityState.EVIDENCE_INCOMPLETE)], "repo", SHA, ["validation"])
    assert matrix["decision"] == "BLOCK"

def test_all_visibility_states_exist():
    assert {x.value for x in obs.VisibilityState} == {"WORKFLOW_VISIBLE", "WORKFLOW_NOT_VISIBLE", "CHECK_VISIBLE", "CHECK_NOT_VISIBLE", "EVIDENCE_COMPLETE", "EVIDENCE_INCOMPLETE"}
