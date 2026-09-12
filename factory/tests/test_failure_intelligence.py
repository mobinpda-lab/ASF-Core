from factory.intelligence.failure import FailureClass, classify_failure


def test_permission_never_enters_ai_repair():
    d = classify_failure("HTTP 403 resource not accessible")
    assert d.category is FailureClass.PERMISSION
    assert d.auto_repair is False
    assert d.retryable is False


def test_provider_pressure_uses_cooldown_not_repair_budget():
    d = classify_failure("OpenAI HTTP 429 too many requests")
    assert d.category is FailureClass.PROVIDER_PRESSURE
    assert d.owner_lane == "PROVIDER_COOLDOWN"
    assert d.auto_repair is False
    assert d.retryable is True


def test_code_failure_can_repair_only_outside_protected_surface():
    safe = classify_failure("SyntaxError compile failed", changed_files=("factory/foo.py",))
    protected = classify_failure("SyntaxError compile failed", changed_files=(".github/workflows/ci.yml",))
    assert safe.category is FailureClass.CODE and safe.auto_repair is True and safe.retryable is True
    assert protected.auto_repair is False and protected.owner_lane == "ESCALATE" and protected.retryable is False


def test_unknown_failure_fails_closed():
    d = classify_failure("strange unclassified event")
    assert d.category is FailureClass.UNKNOWN
    assert d.auto_repair is False
    assert d.retryable is False
