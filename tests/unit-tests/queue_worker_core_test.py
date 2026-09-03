from core.execution.queue_worker import QueueCore, QueueState, WorkerIdentity, WorkerRuntime


class Clock:
    def __init__(self): self.now = 100.0
    def __call__(self): return self.now


def test_enqueue_claim_complete():
    clock = Clock(); queue = QueueCore(clock); task = queue.enqueue({"x": 1}, "t1")
    ctx = queue.claim(WorkerIdentity("w1"))
    assert ctx and ctx.task.task_id == task.task_id
    assert queue.complete(ctx).state is QueueState.SUCCEEDED


def test_expired_lease_is_reclaimed():
    clock = Clock(); queue = QueueCore(clock); queue.enqueue({}, "t1")
    ctx = queue.claim(WorkerIdentity("w1"), lease_seconds=1)
    clock.now += 2
    recovered = queue.reclaim_expired()
    assert recovered[0].state is QueueState.RETRY_WAIT
    assert queue.claim(WorkerIdentity("w2")) is not None


def test_runtime_failure_is_terminal_without_retry_hook():
    clock = Clock(); queue = QueueCore(clock); queue.enqueue({}, "t1")
    class Failing:
        def execute(self, context): raise RuntimeError("boom")
    result = WorkerRuntime(queue, Failing()).run_once(WorkerIdentity("w1"))
    assert result and result.state is QueueState.FAILED


def test_stale_worker_cannot_complete():
    clock = Clock(); queue = QueueCore(clock); queue.enqueue({}, "t1")
    ctx = queue.claim(WorkerIdentity("w1"))
    try:
        queue.complete(type(ctx)(ctx.task, WorkerIdentity("w2"), ctx.lease))
        assert False
    except ValueError as exc:
        assert "lease" in str(exc)
