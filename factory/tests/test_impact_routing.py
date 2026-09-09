from factory.routing.impact import ValidationPath, decide_impact


def test_docs_only_fast():
    d = decide_impact(("README.md", "docs/guide.md"))
    assert d.path is ValidationPath.FAST
    assert d.risk == "LOW"


def test_workflow_change_full():
    d = decide_impact((".github/workflows/ci.yml",))
    assert d.path is ValidationPath.FULL
    assert d.risk == "HIGH"


def test_runtime_change_full():
    d = decide_impact(("src/app.py",))
    assert d.path is ValidationPath.FULL


def test_tests_only_heavy():
    d = decide_impact(("tests/test_worker.py",))
    assert d.path is ValidationPath.HEAVY
