"""Runtime control plane for ASF task intake and governed execution decisions."""
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable, Mapping, Optional

from core.orchestrator.decisions import Decision, FailureClass
from core.state.lifecycle import Lifecycle, LifecycleState

__all__ = ["Decision", "FailureClass", "FailureAction", "Task", "ExecutionContext", "EvidenceRecord", "DecisionRecord", "DependencyEngine", "RecoveryPolicy", "OrchestratorRuntime"]


class FailureAction(str, Enum):
    RETRY = "RETRY"
    WAIT = "WAIT"
    RECOVER = "RECOVER"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class Task:
    task_id: str
    dependencies: tuple[str, ...] = ()
    state: LifecycleState = LifecycleState.CREATED


@dataclass(frozen=True)
class ExecutionContext:
    task_id: str
    context_id: str
    created_at: str
    lifecycle: Lifecycle


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    task_id: str
    complete: bool
    valid: bool = True


@dataclass(frozen=True)
class DecisionRecord:
    decision: Decision
    reason: str
    timestamp: str
    previous_state: LifecycleState
    state_transition: LifecycleState
    task_id: str


class DependencyEngine:
    """Validates dependency completeness and detects cycles."""
    def __init__(self, tasks: Mapping[str, Task]): self.tasks = tasks

    def validate_graph(self) -> None:
        visiting, visited = set(), set()
        def visit(task_id: str) -> None:
            if task_id in visiting: raise ValueError(f"dependency cycle detected at {task_id}")
            if task_id in visited: return
            if task_id not in self.tasks: raise ValueError(f"unknown dependency: {task_id}")
            visiting.add(task_id)
            for dep in self.tasks[task_id].dependencies: visit(dep)
            visiting.remove(task_id); visited.add(task_id)
        for task_id in self.tasks: visit(task_id)

    def ready(self, task_id: str) -> bool:
        self.validate_graph()
        return all(self.tasks[dep].state == LifecycleState.COMPLETED for dep in self.tasks[task_id].dependencies)


class RecoveryPolicy:
    _ACTIONS = {FailureClass.TRANSIENT: FailureAction.RETRY, FailureClass.EVIDENCE: FailureAction.WAIT,
                FailureClass.VALIDATION: FailureAction.RECOVER, FailureClass.GOVERNANCE: FailureAction.BLOCK,
                FailureClass.UNKNOWN: FailureAction.BLOCK}
    def action(self, failure: FailureClass) -> FailureAction: return self._ACTIONS[failure]


class OrchestratorRuntime:
    """Deterministic orchestration runtime; queue/worker execution is out of scope for this wave."""
    def __init__(self, tasks: Iterable[Task] = ()):
        self.tasks = {task.task_id: task for task in tasks}
        self.contexts: dict[str, ExecutionContext] = {}
        self.evidence: dict[str, EvidenceRecord] = {}
        self.history: list[DecisionRecord] = []
        self.dependencies = DependencyEngine(self.tasks)
        for task in self.tasks.values(): self._create_context(task)
        self.recovery = RecoveryPolicy()

    @staticmethod
    def _timestamp() -> str: return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def _create_context(self, task: Task) -> ExecutionContext:
        lifecycle = Lifecycle(task.state)
        context = ExecutionContext(task.task_id, f"ctx-{task.task_id}", self._timestamp(), lifecycle)
        self.contexts[task.task_id] = context
        return context

    def intake(self, task: Task) -> ExecutionContext:
        if not task.task_id.strip(): raise ValueError("task_id is required")
        if task.task_id in self.tasks: raise ValueError(f"duplicate task: {task.task_id}")
        if task.state != LifecycleState.CREATED: raise ValueError("incoming task must start in CREATED state")
        self.tasks[task.task_id] = task
        self.dependencies = DependencyEngine(self.tasks)
        self.dependencies.validate_graph()
        return self._create_context(task)

    def record_evidence(self, record: EvidenceRecord) -> None:
        if record.task_id not in self.tasks: raise ValueError("evidence references unknown task")
        if record.evidence_id in self.evidence: raise ValueError("evidence records are immutable")
        self.evidence[record.evidence_id] = record

    def decide(self, task_id: str, failure: Optional[FailureClass] = None) -> DecisionRecord:
        if task_id not in self.tasks: raise ValueError(f"unknown task: {task_id}")
        context = self.contexts[task_id]
        previous = context.lifecycle.state
        decision, reason, target = Decision.BLOCK, "", previous
        if failure is not None:
            action = self.recovery.action(failure); reason = f"failure={failure.value}; action={action.value}"
            decision = {FailureAction.RETRY: Decision.WAIT, FailureAction.WAIT: Decision.WAIT,
                        FailureAction.RECOVER: Decision.RECOVER, FailureAction.BLOCK: Decision.BLOCK}[action]
            if decision == Decision.RECOVER and previous in {LifecycleState.FAILED, LifecycleState.RUNNING, LifecycleState.VALIDATING}: target = LifecycleState.RECOVERING
        else:
            evidence = next((e for e in self.evidence.values() if e.task_id == task_id), None)
            if not self.dependencies.ready(task_id): decision, reason = Decision.WAIT, "dependency incomplete"
            elif evidence is None or not evidence.complete: decision, reason = Decision.WAIT, "evidence missing or incomplete"
            elif not evidence.valid: decision, reason = Decision.BLOCK, "evidence invalid"
            elif previous not in {LifecycleState.CREATED, LifecycleState.QUEUED, LifecycleState.RUNNING, LifecycleState.VALIDATING, LifecycleState.WAITING_EVIDENCE}: decision, reason = Decision.BLOCK, "invalid execution state"
            else:
                decision, reason = Decision.ALLOW, "dependencies, evidence, and state valid"
                target = LifecycleState.QUEUED if previous == LifecycleState.CREATED else previous
        if target != previous: context.lifecycle.transition(target, reason)
        record = DecisionRecord(decision, reason, self._timestamp(), previous, target, task_id)
        self.history.append(record)
        return record
