from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_nira_is_the_only_canonical_factory_identity() -> None:
    identity = json.loads((ROOT / "NIRA_IDENTITY.json").read_text(encoding="utf-8"))

    assert identity["canonical_name"] == "NIRA"
    assert identity["canonical_repository_identity"] == "NIRA"
    assert identity["repository_name"] == "NIRA"
    assert identity["role"] == "autonomous_software_factory_control_plane"
    assert identity["single_factory_authority"] is True
    assert identity["historical_identifiers_may_be_active_authority"] is False
    assert identity["repository_rename_required"] is False


def test_history_isolated_to_single_record() -> None:
    identity = json.loads((ROOT / "NIRA_IDENTITY.json").read_text(encoding="utf-8"))
    history = ROOT / identity["historical_identity_record"]
    assert history.exists()


def test_active_identity_contract_contains_no_legacy_factory_name() -> None:
    identity = (ROOT / "NIRA_IDENTITY.json").read_text(encoding="utf-8")
    assert "ASF" not in identity
