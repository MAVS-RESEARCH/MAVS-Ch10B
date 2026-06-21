from __future__ import annotations

import csv
from pathlib import Path


def test_metric_rows_align_with_phase3_prediction_indexes() -> None:
    repo_root = Path.cwd()
    for split_label in ("locked", "audit"):
        metric_path = repo_root / "results" / "metrics" / f"{split_label}_corruption" / "metric_rows.csv"
        prediction_path = repo_root / "results" / "stress_runs" / f"phase3_{split_label}_full_v1_prediction_index.csv"
        with metric_path.open("r", encoding="utf-8", newline="") as handle:
            metric_rows = list(csv.DictReader(handle))
        with prediction_path.open("r", encoding="utf-8", newline="") as handle:
            prediction_rows = list(csv.DictReader(handle))
        assert len(metric_rows) == len(prediction_rows)
        metric_keys = {(row["system_id"], row["corruption_id"]) for row in metric_rows}
        prediction_keys = {(row["system_id"], row["corruption_id"]) for row in prediction_rows}
        assert metric_keys == prediction_keys


def test_governance_metrics_have_trace_conditionals() -> None:
    path = Path.cwd() / "results" / "metrics" / "locked_corruption" / "metric_rows.csv"
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["system_id"] in {"veto_mavs", "pure_mavs_gc"}]
    assert rows
    assert all(row["severity_high_unsafe_acceptance_rate"] not in ("", None) for row in rows)
