from __future__ import annotations

import csv
from pathlib import Path


def test_every_stress_run_records_all_specialists() -> None:
    repo_root = Path.cwd()
    expected = "random_forest|gradient_boosted_trees|mlp"
    for run_id in ("phase3_locked_full_v1", "phase3_audit_full_v1"):
        with (repo_root / "results" / "stress_runs" / f"{run_id}_prediction_index.csv").open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        assert rows
        assert all(row["specialist_ids"] == expected for row in rows)
        assert all(int(row["specialist_count"]) == 3 for row in rows)


def test_governance_trace_index_records_all_specialists() -> None:
    repo_root = Path.cwd()
    for run_id in ("phase3_locked_full_v1", "phase3_audit_full_v1"):
        with (repo_root / "results" / "stress_runs" / f"{run_id}_trace_index.csv").open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        assert rows
        assert all(int(row["specialist_count"]) == 3 for row in rows)
