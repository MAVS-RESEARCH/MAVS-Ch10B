from __future__ import annotations

import csv
import json
from pathlib import Path


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_phase5_required_outputs_exist_and_have_expected_rows() -> None:
    repo_root = Path.cwd()
    required = [
        repo_root / "configs" / "reports" / "robustness_report.yaml",
        repo_root / "results" / "reports" / "robustness_report.md",
        repo_root / "results" / "reports" / "corruption_atlas.md",
        repo_root / "results" / "reports" / "failure_map.md",
        repo_root / "results" / "reports" / "robustness_tables.csv",
        repo_root / "results" / "reports" / "robustness_system_deltas.csv",
        repo_root / "results" / "reports" / "robustness_reproducibility_manifest.json",
        repo_root / "results" / "figures" / "governance_severity_distribution.png",
        repo_root / "results" / "figures" / "threshold_distribution.png",
        repo_root / "results" / "figures" / "unsafe_acceptance_by_corruption.png",
        repo_root / "results" / "figures" / "robustness_area_by_system.png",
    ]
    for path in required:
        assert path.exists(), path
        assert path.stat().st_size > 0, path
    assert len(_rows(repo_root / "results" / "reports" / "robustness_tables.csv")) == 90900
    assert len(_rows(repo_root / "results" / "reports" / "robustness_system_deltas.csv")) == 100800


def test_phase5_manifest_row_counts_match_generated_tables() -> None:
    repo_root = Path.cwd()
    manifest = json.loads((repo_root / "results" / "reports" / "robustness_reproducibility_manifest.json").read_text(encoding="utf-8"))
    assert manifest["row_counts"]["metric_rows"] == 14400
    assert manifest["row_counts"]["area_rows"] == 3600
    assert manifest["row_counts"]["robustness_table_rows"] == 90900
    assert manifest["row_counts"]["system_delta_rows"] == 100800
    assert manifest["run_modes"] == ["exploratory"]


def test_phase5_system_deltas_include_veto_baseline_for_pure_mavs_gc() -> None:
    rows = _rows(Path.cwd() / "results" / "reports" / "robustness_system_deltas.csv")
    assert any(row["subject_system_id"] == "pure_mavs_gc" and row["baseline_system_id"] == "veto_mavs" for row in rows)
    assert any(row["subject_system_id"] == "veto_mavs" and row["baseline_system_id"] == "mean_ensemble" for row in rows)
