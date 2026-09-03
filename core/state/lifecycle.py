from dataclasses import dataclass
from enum import Enum
from typing import Optional

class LifecycleState(str, Enum):
    CREATED="CREATED"; QUEUED="QUEUED"; RUNNING="RUNNING"; VALIDATING="VALIDATING"; WAITING_EVIDENCE="WAITING_EVIDENCE"; READY="READY"; FAILED="FAILED"; RECOVERING="RECOVERING"; COMPLETED="COMPLETED"

_ALLOWED={
 LifecycleState.CREATED:{LifecycleState.QUEUED, LifecycleState.FAILED},
 LifecycleState.QUEUED:{LifecycleState.RUNNING, LifecycleState.FAILED},
 LifecycleState.RUNNING:{LifecycleState.VALIDATING, LifecycleState.FAILED, LifecycleState.RECOVERING},
 LifecycleState.VALIDATING:{LifecycleState.WAITING_EVIDENCE, LifecycleState.READY, LifecycleState.FAILED, LifecycleState.RECOVERING},
 LifecycleState.WAITING_EVIDENCE:{LifecycleState.READY, LifecycleState.FAILED, LifecycleState.RECOVERING},
 LifecycleState.READY:{LifecycleState.COMPLETED, LifecycleState.FAILED},
 LifecycleState.FAILED:{LifecycleState.RECOVERING, LifecycleState.COMPLETED},
 LifecycleState.RECOVERING:{LifecycleState.QUEUED, LifecycleState.RUNNING, LifecycleState.FAILED},
 LifecycleState.COMPLETED:set(),
}

@dataclass(frozen=True)
class StateTransition:
    previous: LifecycleState
    current: LifecycleState
    reason: str
    evidence_id: Optional[str]=None

class Lifecycle:
    def __init__(self, state=LifecycleState.CREATED): self.state=state; self.history=()
    def transition(self, target, reason, evidence_id=None):
        target=LifecycleState(target)
        if target not in _ALLOWED[self.state]: raise ValueError(f"invalid transition: {self.state}->{target}")
        self.history=self.history+(StateTransition(self.state,target,reason,evidence_id),); self.state=target
        return self.state
