import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_worker_provider_order_is_gemini_openrouter_then_openai():
    worker = read(".github/workflows/nira-cross-repo-worker.yml")
    router = read("factory/runtime/provider_router.js")
    assert "gemini,openrouter,openai" in worker
    assert "NIRA_PROVIDER_ORDER" in worker
    assert "GEMINI_API_KEY" in worker
    assert "OPENROUTER_API_KEY" in worker
    assert "OPENAI_API_KEY" in worker
    assert "gemini,openrouter,openai" in router


def test_router_uses_current_provider_endpoints_and_free_openrouter_default():
    router = read("factory/runtime/provider_router.js")
    assert "generativelanguage.googleapis.com/v1beta/models/" in router
    assert ":generateContent" in router
    assert "https://openrouter.ai/api/v1/chat/completions" in router
    assert "openrouter/free" in router
    assert "https://api.openai.com/v1/responses" in router


def test_router_fails_over_before_declaring_global_capacity_exhaustion():
    router = read("factory/runtime/provider_router.js")
    assert "for (const provider of providers)" in router
    assert "NIRA_PROVIDER_FAILOVER" in router
    assert "attempts.every(item => item.exhausted)" in router
    assert "NIRA_PROVIDER_CAPACITY_EXHAUSTED" in router
    assert "NIRA_PROVIDER_ROUTER_FAILED" in router
    assert "NIRA_BLOCKED=NO_AI_PROVIDER_CONFIGURED" in router


def test_router_retries_transport_failure_on_same_provider_with_hard_bound():
    router = read("factory/runtime/provider_router.js")
    assert "NIRA_PROVIDER_ATTEMPTS_PER_PROVIDER" in router
    assert "Math.max(1, Math.min(Math.floor(configured), 3))" in router
    assert "providerAttempt <= maxProviderAttempts" in router
    assert "NIRA_PROVIDER_RETRY" in router
    assert "retryableSameProviderFailure" in router
    assert "status === 0 || [502, 503, 504].includes(status)" in router
    # A 429 is intentionally not retried on the same provider; the existing
    # cooldown/failover authority handles provider pressure without storms.
    retry_function = router.split("function retryableSameProviderFailure", 1)[1].split("function delay", 1)[0]
    assert "429" not in retry_function


def test_scheduler_accepts_any_configured_provider_not_only_openai():
    scheduler = read(".github/workflows/nira-queue-scheduler.yml")
    availability = next(
        line for line in scheduler.splitlines()
        if line.strip().startswith("NIRA_AI_PROVIDER_AVAILABLE:")
    )
    assert "GEMINI_API_KEY" in availability
    assert "OPENROUTER_API_KEY" in availability
    assert "OPENAI_API_KEY" in availability
    assert "||" in availability


def test_capacity_probe_uses_same_router_and_can_restore_from_any_provider():
    probe = read(".github/workflows/nira-provider-capacity-probe.yml")
    assert "provider_router.js" in probe
    assert "routedResponse" in probe
    assert "configuredProviderNames" in probe
    assert "GEMINI_API_KEY" in probe
    assert "OPENROUTER_API_KEY" in probe
    assert "OPENAI_API_KEY" in probe
    assert "NIRA_PROVIDER_CAPACITY=RESTORED" in probe
    assert "PROVIDER=' + probe.provider" in probe


def test_self_completion_worker_enforces_exact_scope_before_model_selection():
    runtime = read("factory/runtime/bounded_worker.js")
    assert "extractExactScope" in runtime
    assert "NIRA_SELF_COMPLETION_TASK: true" in runtime
    assert "selection contains unknown or out-of-scope path" in runtime
    assert "changed.push({ path: patch.path" in runtime


def test_multi_provider_runtime_is_protected_factory_authority():
    policy = json.loads(read("factory/registry/autonomous-mutation-policy.json"))
    protected = set(policy["protected_paths"])
    assert "factory/runtime/provider_router.js" in protected
    assert "factory/runtime/bounded_worker.js" in protected
    assert policy["safety"]["multi_provider_failover_is_bounded"] is True
    assert policy["safety"]["openai_is_optional"] is True
