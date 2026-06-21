from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from mavs_ch10b.evaluation.metrics import metrics_from_arrays


def test_accuracy_and_f1_use_clean_labels() -> None:
    decisions = np.array([1, 1, 0, 0], dtype=np.int8)
    y_clean = np.array([1, 0, 1, 0], dtype=np.int8)
    y_observed = np.array([0, 0, 1, 1], dtype=np.int8)
    metrics = metrics_from_arrays(decisions=decisions, y_clean=y_clean, y_observed=y_observed, corruption_level=0.4)
    assert metrics.accuracy == 0.5
    assert metrics.f1 == 0.5
    assert metrics.observed_label_accuracy == 0.0


def test_metric_rows_exist_for_both_splits() -> None:
    repo_root = Path.cwd()
    for split_label in ("locked", "audit"):
        path = repo_root / "results" / "metrics" / f"{split_label}_corruption" / "metric_rows.csv"
        assert path.exists()
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        assert len(rows) == 7200
        assert all(row["technical_failure_rate"] == "0.0" for row in rows)
        assert all(row["high_corruption_unsafe_acceptance_rate"] != "" for row in rows)
