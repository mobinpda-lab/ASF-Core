from factory.feedback.provider_pressure import classify_provider_pressure, pressure_allows_retry


def test_rate_limit_is_bounded_and_retryable():
    decision = classify_provider_pressure(status_code=429, retry_after_seconds=9999)
    assert decision is not None
    assert decision.category == "PROVIDER_RATE_LIMIT"
    assert decision.retryable is True
    assert decision.retry_after_seconds == 300
    assert pressure_allows_retry(decision, attempt=0, max_attempts=2) is True
    assert pressure_allows_retry(decision, attempt=2, max_attempts=2) is False


def test_upstream_unavailable_has_bounded_backoff():
    decision = classify_provider_pressure(status_code=503)
    assert decision is not None
    assert decision.category == "PROVIDER_UNAVAILABLE"
    assert decision.retryable is True
    assert decision.retry_after_seconds == 15


def test_routing_422_never_enters_blind_retry_loop():
    decision = classify_provider_pressure(status_code=422)
    assert decision is not None
    assert decision.category == "PROVIDER_ROUTING_REJECTED"
    assert decision.retryable is False
    assert pressure_allows_retry(decision, attempt=0) is False


def test_unknown_failure_is_not_reclassified_as_provider_pressure():
    assert classify_provider_pressure(status_code=400, message="bad request") is None
