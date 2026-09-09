from factory.routing.worker_roles import CONTRACTS, WorkerRole, infer_role


def test_specialized_roles_exist_without_competing_promotion_authority():
    assert set(CONTRACTS) == set(WorkerRole)
    assert all(contract.promotion_allowed is False for contract in CONTRACTS.values())


def test_only_bounded_mutation_roles_can_write():
    assert CONTRACTS[WorkerRole.DEVELOPMENT].mutation_allowed is True
    assert CONTRACTS[WorkerRole.DOCUMENTATION].mutation_allowed is True
    for role in (WorkerRole.ARCHITECT, WorkerRole.TESTING, WorkerRole.REVIEW, WorkerRole.RELEASE, WorkerRole.RECOVERY):
        assert CONTRACTS[role].mutation_allowed is False


def test_role_routing_is_deterministic():
    assert infer_role("architecture: design API") is WorkerRole.ARCHITECT
    assert infer_role("test: regression suite") is WorkerRole.TESTING
    assert infer_role("security review") is WorkerRole.REVIEW
    assert infer_role("docs: README") is WorkerRole.DOCUMENTATION
    assert infer_role("release: publish artifact") is WorkerRole.RELEASE
    assert infer_role("[AUTO-FIX] CI failure") is WorkerRole.RECOVERY
    assert infer_role("feat: implement queue") is WorkerRole.DEVELOPMENT
