"""Provider-independent queue/worker execution primitives."""
from dataclasses import dataclass, field, replace
from enum import Enum
from time import time
from typing import Callable, Mapping, Optional, Protocol
from uuid import uuid4


class QueueState(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    RETRY_WAIT = "RETRY_WAIT"
    RECOVERING = "RECOVERING"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class Task:
    task_id: str
    payload: Mapping[str, object]
    state: QueueState = QueueState.QUEUED
    attempts: int = 0
    available_at: float = 0.0
    lease_id: Optional[str] = None


@dataclass(frozen=True)
class Lease:
    lease_id: str
    task_id: str
    worker_id: str
    expires_at: float


@dataclass(frozen=True)
class WorkerIdentity:
    worker_id: str = field(default_factory=lambda: f"worker-{uuid4()}")
    runtime: str = "asf-core"


@dataclass(frozen=True)
class ExecutionContext:
    task: Task
    worker: WorkerIdentity
    lease: Lease


class Worker(Protocol):
    def execute(self, context: ExecutionContext) -> None: ...


class QueueCore:
    """Deterministic in-memory queue core; persistence belongs to an adapter."""
    def __init__(self, clock: Callable[[], float] = time) -> None:
        self._clock = clock
        self._tasks: dict[str, Task] = {}
        self._leases: dict[str, Lease] = {}

    def enqueue(self, payload: Mapping[str, object], task_id: Optional[str] = None) -> Task:
        task = Task(task_id or str(uuid4()), payload, available_at=self._clock())
        if task.task_id in self._tasks:
            raise ValueError("task_id already exists")
        self._tasks[task.task_id] = task
        return task

    def claim(self, worker: WorkerIdentity, lease_seconds: float = 60.0) -> Optional[ExecutionContext]:
        now = self._clock()
        candidates = [t for t in self._tasks.values() if t.state in {QueueState.QUEUED, QueueState.RETRY_WAIT} and t.available_at <= now]
        if not candidates:
            return None
        task = sorted(candidates, key=lambda t: (t.available_at, t.task_id))[0]
        lease = Lease(str(uuid4()), task.task_id, worker.worker_id, now + lease_seconds)
        claimed = replace(task, state=QueueState.RUNNING, attempts=task.attempts + 1, lease_id=lease.lease_id)
        self._tasks[task.task_id] = claimed
        self._leases[lease.lease_id] = lease
        return ExecutionContext(claimed, worker, lease)

    def complete(self, context: ExecutionContext) -> Task:
        self._assert_lease(context)
        task = replace(self._tasks[context.task.task_id], state=QueueState.SUCCEEDED, lease_id=None)
        self._tasks[task.task_id] = task
        self._leases.pop(context.lease.lease_id, None)
        return task

    def fail(self, context: ExecutionContext, retry_at: Optional[float] = None) -> Task:
        self._assert_lease(context)
        state = QueueState.RETRY_WAIT if retry_at is not None else QueueState.FAILED
        available_at = retry_at if retry_at is not None else self._clock()
        task = replace(self._tasks[context.task.task_id], state=state, available_at=available_at, lease_id=None)
        self._tasks[task.task_id] = task
        self._leases.pop(context.lease.lease_id, None)
        return task

    def reclaim_expired(self) -> tuple[Task, ...]:
        now = self._clock()
        expired = [l for l in self._leases.values() if l.expires_at <= now]
        recovered = []
        for lease in expired:
            task = self._tasks[lease.task_id]
            recovered_task = replace(task, state=QueueState.RECOVERING, lease_id=None, available_at=now)
            self._tasks[task.task_id] = replace(recovered_task, state=QueueState.RETRY_WAIT)
            self._leases.pop(lease.lease_id, None)
            recovered.append(self._tasks[task.task_id])
        return tuple(recovered)

    def get(self, task_id: str) -> Task:
        return self._tasks[task_id]

    def _assert_lease(self, context: ExecutionContext) -> None:
        lease = self._leases.get(context.lease.lease_id)
        if lease is None or lease.task_id != context.task.task_id or lease.worker_id != context.worker.worker_id:
            raise ValueError("invalid or stale lease")
        if lease.expires_at <= self._clock():
            raise ValueError("expired lease")


class TaskScheduler:
    def __init__(self, queue: QueueCore) -> None:
        self.queue = queue

    def next(self, worker: WorkerIdentity, lease_seconds: float = 60.0) -> Optional[ExecutionContext]:
        self.queue.reclaim_expired()
        return self.queue.claim(worker, lease_seconds)


class WorkerRuntime:
    def __init__(self, queue: QueueCore, worker: Worker) -> None:
        self.queue = queue
        self.worker = worker

    def run_once(self, worker: WorkerIdentity) -> Optional[Task]:
        context = TaskScheduler(self.queue).next(worker)
        if context is None:
            return None
        try:
            self.worker.execute(context)
            return self.queue.complete(context)
        except Exception:
            return self.queue.fail(context)
