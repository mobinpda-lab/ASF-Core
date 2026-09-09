from factory.scheduling.adaptive import CapacitySnapshot, decide_ai_capacity


def snap(**kw):
    base = dict(queued_ai=0, success_rate=1.0, provider_pressure=0, repeated_failures=0, active_ai=0)
    base.update(kw)
    return CapacitySnapshot(**base)


def test_scales_up_only_on_healthy_backlog():
    d = decide_ai_capacity(snap(queued_ai=6, success_rate=0.96), current=1, maximum=4)
    assert d.max_ai_leases == 2
    assert d.reason == "HEALTHY_BACKLOG"


def test_provider_pressure_scales_down():
    d = decide_ai_capacity(snap(queued_ai=8, provider_pressure=1), current=3)
    assert d.max_ai_leases == 2


def test_repeated_failures_scale_down():
    d = decide_ai_capacity(snap(queued_ai=8, repeated_failures=3), current=2)
    assert d.max_ai_leases == 1


def test_capacity_is_bounded():
    d = decide_ai_capacity(snap(queued_ai=100, success_rate=1.0), current=4, maximum=4)
    assert d.max_ai_leases == 4
