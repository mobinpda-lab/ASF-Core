from factory.feedback.failure_feedback import Failure, FailureFeedback


def failure(*, attempt: int = 0, retryable: bool = True) -> Failure:
    return Failure("task-1", attempt, "VALIDATION", retryable, "evidence-1")


def test_retryable_failure_enters_bounded_auto_fix():
    decision = FailureFeedback(max_auto_fix_attempts=2).decide(failure())
    assert decision.action == "AUTO_FIX"
    assert decision.reason == "BOUNDED_RETRYABLE_FAILURE"


def test_non_retryable_failure_escalates():
    decision = FailureFeedback().decide(failure(retryable=False))
    assert decision.action == "ESCALATE"
    assert decision.reason == "NON_RETRYABLE"


def test_budget_exhaustion_escalates():
    decision = FailureFeedback(max_auto_fix_attempts=2).decide(failure(attempt=2))
    assert decision.action == "ESCALATE"
    assert decision.reason == "AUTO_FIX_BUDGET_EXHAUSTED"


def test_duplicate_failure_is_suppressed():
    feedback = FailureFeedback()
    first = feedback.decide(failure())
    second = feedback.decide(failure())
    assert first.action == "AUTO_FIX"
    assert second.action == "SUPPRESS"
    assert second.reason == "DUPLICATE_FAILURE"
