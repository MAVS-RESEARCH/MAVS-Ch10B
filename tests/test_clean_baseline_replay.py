from __future__ import annotations

import csv
from pathlib import Path


def test_clean_replay_artifacts_show_zero_mismatches() -> None:
    repo_root = Path.cwd()
    manifest_path = repo_root / "results" / "baseline_import" / "clean_replay_manifest.json"
    comparison_path = repo_root / "results" / "baseline_import" / "clean_replay_comparison.csv"
    metrics_path = repo_root / "results" / "baseline_import" / "clean_replay_metrics.csv"
    assert manifest_path.exists()
    assert comparison_path.exists()
    assert metrics_path.exists()
    with comparison_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 360
    assert {row["status"] for row in rows} == {"pass"}
    with metrics_path.open("r", encoding="utf-8", newline="") as handle:
        metric_rows = list(csv.DictReader(handle))
    assert len(metric_rows) == 40

