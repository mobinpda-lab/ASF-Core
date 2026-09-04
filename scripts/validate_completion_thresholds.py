#!/usr/bin/env python3
"""Fail-closed validation for ASF completion thresholds and runtime metrics."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "factory" / "completion-thresholds.json"


def fail(message: str) -> "NoReturn":
    print(f"BLOCK: {message}")
    raise SystemExit(1)


def require(metrics: dict, key: str):
    if key not in metrics:
        fail(f"missing metric: {key}")
    return metrics[key]


def rate(metrics: dict, key: str, minimum: float, sample_min: int) -> None:
    value = require(metrics, key)
    sample = require(metrics, f"{key}.sample")
    if sample < sample_min:
        fail(f"{key}: sample={sample} < minimum={sample_min}")
    if value < minimum:
        fail(f"{key}: value={value} < minimum={minimum}")


def maximum(metrics: dict, key: str, maximum_value: float) -> None:
    value = require(metrics, key)
    if value > maximum_value:
        fail(f"{key}: value={value} > maximum={maximum_value}")


def load_contract() -> dict:
    try:
        contract = json.loads(CONTRACT.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid threshold contract: {exc}")
    if contract.get("version") != "1.0.0":
        fail("unsupported threshold contract version")
    return contract


def validate_contract_shape(contract: dict) -> None:
    required_sections = {"critical", "factory", "evidence", "products", "ncm_control_plane", "completion"}
    if set(contract) != {"version", *required_sections}:
        fail("threshold contract has unexpected/missing top-level sections")
    for section, rules in contract.items():
        if section == "version":
            continue
        if not isinstance(rules, dict) or not rules:
            fail(f"empty threshold section: {section}")
        for key, rule in rules.items():
            if not isinstance(rule, dict):
                fail(f"invalid rule: {section}.{key}")
            if "min" not in rule and "max" not in rule and "min_count" not in rule:
                fail(f"rule has no bound: {section}.{key}")
            if "min" in rule and "max" in rule and rule["min"] > rule["max"]:
                fail(f"contradictory bounds: {section}.{key}")
            if "sample_min" in rule and rule["sample_min"] < 1:
                fail(f"invalid sample_min: {section}.{key}")


def validate_metrics(metrics: dict, contract: dict) -> None:
    critical = contract["critical"]
    factory = contract["factory"]
    evidence = contract["evidence"]
    products = contract["products"]
    ncm = contract["ncm_control_plane"]
    completion = contract["completion"]

    for key in ("governance_violations", "manual_merges", "direct_main_writes", "force_pushes", "unknown_promotions"):
        maximum(metrics, key, critical[key]["max"])
    rate(metrics, "exact_sha_match_rate", critical["exact_sha_match_rate"]["min"], critical["exact_sha_match_rate"]["sample_min"])
    rate(metrics, "promotion_success_rate", critical["promotion_success_rate"]["min"], critical["promotion_success_rate"]["sample_min"])

    rate(metrics, "registry_coverage", factory["registry_coverage"]["min"], 1)
    rate(metrics, "dependency_coverage", factory["dependency_coverage"]["min"], 1)
    maximum(metrics, "duplicate_active_tasks", factory["duplicate_active_tasks"]["max"])
    maximum(metrics, "duplicate_worker_leases", factory["duplicate_worker_leases"]["max"])
    waves = require(metrics, "wave_widths")
    if len(waves) < factory["parallel_waves"]["min"] or any(w < factory["min_parallel_tasks_per_wave"]["min"] for w in waves[-factory["parallel_waves"]["min"]:]):
        fail("parallel wave evidence does not meet width/count threshold")
    rate(metrics, "worker_success_rate", factory["worker_success_rate"]["min"], factory["worker_success_rate"]["sample_min"])
    rate(metrics, "task_completion_rate", factory["task_completion_rate"]["min"], factory["task_completion_rate"]["sample_min"])
    rate(metrics, "recovery_success_rate", factory["recovery_success_rate"]["min"], factory["recovery_success_rate"]["sample_min"])
    maximum(metrics, "queue_refill_p95_seconds", factory["queue_refill_p95_seconds"]["max"])
    maximum(metrics, "recovery_p95_seconds", factory["recovery_p95_seconds"]["max"])
    maximum(metrics, "parallel_speed_ratio", factory["parallel_speed_ratio"]["max"])

    rate(metrics, "evidence_completeness_rate", evidence["evidence_completeness_rate"]["min"], evidence["evidence_completeness_rate"]["sample_min"])
    maximum(metrics, "evidence_freshness_p95_seconds", evidence["evidence_freshness_p95_seconds"]["max"])
    maximum(metrics, "expired_artifacts", evidence["expired_artifacts"]["max"])

    if require(metrics, "registered_repositories") < products["required_repositories"]["min_count"]:
        fail("required product repositories not registered")
    rate(metrics, "cross_repo_ingestion_rate", products["cross_repo_ingestion_rate"]["min"], products["cross_repo_ingestion_rate"]["sample_min"])
    maximum(metrics, "wrong_repo_routing", products["wrong_repo_routing"]["max"])
    maximum(metrics, "orphan_tasks", products["orphan_tasks"]["max"])

    if require(metrics, "ncm_e2e_cycles") < ncm["e2e_cycles"]["min"]:
        fail("NCM E2E cycle threshold not reached")
    rate(metrics, "ncm_ingestion_rate", ncm["ingestion_rate"]["min"], ncm["ingestion_rate"]["sample_min"])
    rate(metrics, "diagnosis_rate", ncm["diagnosis_rate"]["min"], ncm["diagnosis_rate"]["sample_min"])
    rate(metrics, "control_trigger_rate", ncm["control_trigger_rate"]["min"], ncm["control_trigger_rate"]["sample_min"])
    rate(metrics, "ncm_recovery_rate", ncm["recovery_rate"]["min"], ncm["recovery_rate"]["sample_min"])
    maximum(metrics, "orphan_events", ncm["orphan_events"]["max"])
    maximum(metrics, "unclassified_events", ncm["unclassified_events"]["max"])

    for key, rule in completion.items():
        maximum(metrics, key, rule["max"])


def main() -> int:
    contract = load_contract()
    validate_contract_shape(contract)
    if len(sys.argv) == 2 and sys.argv[1] == "--contract-only":
        print("PASS: completion threshold contract is valid")
        return 0
    if len(sys.argv) != 2:
        fail("usage: validate_completion_thresholds.py --contract-only | METRICS.json")
    try:
        metrics = json.loads(Path(sys.argv[1]).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid metrics JSON: {exc}")
    validate_metrics(metrics, contract)
    print("PASS: operational completion thresholds satisfied")
    return 0


if __name__ == "__main__":
    main()
