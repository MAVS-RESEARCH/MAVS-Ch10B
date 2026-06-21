from __future__ import annotations

import json
from pathlib import Path


def test_corruption_atlas_covers_every_required_family() -> None:
    repo_root = Path.cwd()
    manifest = json.loads((repo_root / "results" / "corruption_manifests" / "corruption_grid_manifest.json").read_text(encoding="utf-8"))
    text = (repo_root / "results" / "reports" / "corruption_atlas.md").read_text(encoding="utf-8")
    for family in manifest["corruption_families"]:
        assert f"## {family}" in text
    assert text.count("### Implementation Definition") == len(manifest["corruption_families"])
    assert text.count("### Parameterization") == len(manifest["corruption_families"])
    assert text.count("### Affected Target Space") == len(manifest["corruption_families"])
    assert text.count("### Expected Failure Mode") == len(manifest["corruption_families"])
    assert text.count("### Observed Degradation Pattern") == len(manifest["corruption_families"])
    assert text.count("### Best and Worst Systems") == len(manifest["corruption_families"])
    assert text.count("### Linked Artifacts") == len(manifest["corruption_families"])


def test_corruption_atlas_links_phase4_artifacts() -> None:
    text = (Path.cwd() / "results" / "reports" / "corruption_atlas.md").read_text(encoding="utf-8")
    assert "results/metrics/locked_corruption/metric_rows.csv" in text
    assert "results/metrics/audit_corruption/metric_rows.csv" in text
    assert "results/robustness_curves/robustness_curve_area.csv" in text
