from core.execution.queue_worker import QueueCore, QueueState, TaskScheduler, WorkerIdentity, WorkerRuntime


class Clock:
    def __init__(self): self.now = 100.0
    def __call__(self): return self.now


def test_enqueue_claim_complete():
    clock = Clock(); queue = QueueCore(clock); task = queue.enqueue({"x": 1}, "t1")
    ctx = queue.claim(WorkerIdentity("w1"))
    assert ctx and ctx.task.task_id == task.task_id
    assert ctx.task.attempts == 1
    assert queue.complete(ctx).state is QueueState.SUCCEEDED


def test_scheduler_reclaims_expired_lease_for_another_worker():
    clock = Clock(); queue = QueueCore(clock); queue.enqueue({}, "t1")
    queue.claim(WorkerIdentity("w1"), lease_seconds=1)
    clock.now += 2
    ctx = TaskScheduler(queue).next(WorkerIdentity("w2"))
    assert ctx is not None
    assert ctx.worker.worker_id == "w2"
    assert ctx.task.state is QueueState.RUNNING
    assert ctx.task.attempts == 2


def test_retry_wait_respects_explicit_zero_timestamp():
    clock = Clock(); queue = QueueCore(clock); queue.enqueue({}, "t1")
    ctx = queue.claim(WorkerIdentity("w1"))
    result = queue.fail(ctx, retry_at=0.0)
    assert result.state is QueueState.RETRY_WAIT
    assert result.available_at == 0.0


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


def test_expired_lease_cannot_complete():
    clock = Clock(); queue = QueueCore(clock); queue.enqueue({}, "t1")
    ctx = queue.claim(WorkerIdentity("w1"), lease_seconds=1)
    clock.now += 1
    try:
        queue.complete(ctx)
        assert False
    except ValueError as exc:
        assert "expired" in str(exc)
