from __future__ import annotations

import json
from pathlib import Path


def test_failure_map_contains_required_sections() -> None:
    text = (Path.cwd() / "results" / "reports" / "failure_map.md").read_text(encoding="utf-8")
    required_sections = [
        "## Executive Failure Summary",
        "## When Pure MAVS-GC Fails",
        "## When Veto MAVS Fails",
        "## Governance Over-Rejection",
        "## Governance Under-Rejection",
        "## Unsafe Acceptance Survives",
        "## Most Damaging Corruption Families",
        "## Failure Mechanism Classification",
        "## Linked Artifacts",
    ]
    for section in required_sections:
        assert section in text
    assert "specialist_failure" in text
    assert "Veto MAVS vs Mean Ensemble average accuracy delta" in text


def test_failure_map_classifies_every_corruption_family() -> None:
    repo_root = Path.cwd()
    manifest = json.loads((repo_root / "results" / "corruption_manifests" / "corruption_grid_manifest.json").read_text(encoding="utf-8"))
    text = (repo_root / "results" / "reports" / "failure_map.md").read_text(encoding="utf-8")
    for family in manifest["corruption_families"]:
        assert f"`{family}`:" in text
