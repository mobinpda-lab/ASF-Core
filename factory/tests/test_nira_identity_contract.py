from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_nira_is_the_only_canonical_factory_identity() -> None:
    identity = json.loads((ROOT / "NIRA_IDENTITY.json").read_text(encoding="utf-8"))

    assert identity["canonical_name"] == "NIRA"
    assert identity["canonical_repository_identity"] == "NIRA"
    assert identity["role"] == "autonomous_software_factory_control_plane"
    assert identity["single_factory_authority"] is True
    assert identity["historical_identifiers_may_be_active_authority"] is False


def test_legacy_names_are_explicitly_historical() -> None:
    identity = json.loads((ROOT / "NIRA_IDENTITY.json").read_text(encoding="utf-8"))

    assert set(identity["historical_identifiers"]) == {"ASF-Core", "ASF-MOC"}
    assert identity["current_github_repository"] == "mobinpda-lab/ASF-Core"
    assert identity["repository_rename_required"] is True
