import unittest

from core.orchestrator.runtime import Decision, EvidenceRecord, FailureAction, FailureClass, OrchestratorRuntime, Task
from core.state.lifecycle import LifecycleState


class RuntimeTests(unittest.TestCase):
    def test_intake_creates_context(self):
        runtime = OrchestratorRuntime()
        ctx = runtime.intake(Task("t1"))
        self.assertEqual(ctx.lifecycle.state, LifecycleState.CREATED)
        self.assertEqual(ctx.task_id, "t1")

    def test_dependency_blocks_until_complete(self):
        runtime = OrchestratorRuntime([Task("a", state=LifecycleState.COMPLETED), Task("b", ("a",))])
        runtime.record_evidence(EvidenceRecord("e-b", "b", True))
        result = runtime.decide("b")
        self.assertEqual(result.decision, Decision.ALLOW)
        self.assertEqual(result.reason, "dependencies, evidence, and state valid")

    def test_incomplete_dependency_waits(self):
        runtime = OrchestratorRuntime([Task("a"), Task("b", ("a",))])
        runtime.record_evidence(EvidenceRecord("e-b", "b", True))
        result = runtime.decide("b")
        self.assertEqual(result.decision, Decision.WAIT)
        self.assertEqual(result.reason, "dependency incomplete")

    def test_evidence_missing_waits(self):
        runtime = OrchestratorRuntime()
        runtime.intake(Task("t1"))
        result = runtime.decide("t1")
        self.assertEqual(result.decision, Decision.WAIT)
        self.assertIn("evidence", result.reason)

    def test_allow_transitions_created_to_queued(self):
        runtime = OrchestratorRuntime()
        runtime.intake(Task("t1"))
        runtime.record_evidence(EvidenceRecord("e1", "t1", True, True))
        result = runtime.decide("t1")
        self.assertEqual(result.decision, Decision.ALLOW)
        self.assertEqual(result.previous_state, LifecycleState.CREATED)
        self.assertEqual(result.state_transition, LifecycleState.QUEUED)
        self.assertEqual(runtime.contexts["t1"].lifecycle.state, LifecycleState.QUEUED)

    def test_failure_recovery_mapping(self):
        runtime = OrchestratorRuntime()
        self.assertEqual(runtime.recovery.action(FailureClass.TRANSIENT), FailureAction.RETRY)
        self.assertEqual(runtime.recovery.action(FailureClass.EVIDENCE), FailureAction.WAIT)
        self.assertEqual(runtime.recovery.action(FailureClass.VALIDATION), FailureAction.RECOVER)
        self.assertEqual(runtime.recovery.action(FailureClass.GOVERNANCE), FailureAction.BLOCK)
        self.assertEqual(runtime.recovery.action(FailureClass.UNKNOWN), FailureAction.BLOCK)

    def test_invalid_dependency_cycle(self):
        runtime = OrchestratorRuntime([Task("a", ("b",)), Task("b", ("a",))])
        with self.assertRaises(ValueError):
            runtime.dependencies.validate_graph()

    def test_invalid_transition_rejected(self):
        runtime = OrchestratorRuntime()
        runtime.intake(Task("t1"))
        with self.assertRaises(ValueError):
            runtime.contexts["t1"].lifecycle.transition(LifecycleState.COMPLETED, "illegal")

    def test_evidence_is_immutable(self):
        runtime = OrchestratorRuntime()
        runtime.intake(Task("t1"))
        runtime.record_evidence(EvidenceRecord("e1", "t1", True))
        with self.assertRaises(ValueError):
            runtime.record_evidence(EvidenceRecord("e1", "t1", True))


if __name__ == "__main__":
    unittest.main()
