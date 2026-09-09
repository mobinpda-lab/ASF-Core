from factory.scheduling.policy import CapacityPolicy, ExecutionLane, execution_lane, priority_rank


def test_priority_orders_release_and_core_before_feature():
    assert priority_rank({"priority:release-blocker"}) == 0
    assert priority_rank({"priority:core"}) == 1
    assert priority_rank({"priority:automation"}) == 2
    assert priority_rank({"priority:feature"}) == 3
    assert priority_rank(set()) == 4
    assert priority_rank({"priority:feature", "priority:core"}) == 1


def test_execution_lane_is_explicit_and_provider_neutral():
    assert execution_lane("NIRA_EXECUTION_MODE: deterministic-doc-append") is ExecutionLane.DETERMINISTIC
    assert execution_lane("ordinary bounded implementation") is ExecutionLane.AI


def test_capacity_serializes_ai_but_allows_parallel_deterministic_work():
    policy = CapacityPolicy(max_ai_leases=1, max_deterministic_leases=4)
    assert policy.available(ExecutionLane.AI, active_ai=0, active_deterministic=3) == 1
    assert policy.available(ExecutionLane.AI, active_ai=1, active_deterministic=0) == 0
    assert policy.available(ExecutionLane.DETERMINISTIC, active_ai=1, active_deterministic=1) == 3
