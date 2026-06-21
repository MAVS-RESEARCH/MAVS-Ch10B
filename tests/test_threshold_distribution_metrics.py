from __future__ import annotations

import csv
from pathlib import Path


def test_governance_severity_and_threshold_distributions_exist() -> None:
    repo_root = Path.cwd()
    for split_label in ("locked", "audit"):
        severity_path = repo_root / "results" / "metrics" / f"{split_label}_corruption" / "governance_severity_distribution.csv"
        threshold_path = repo_root / "results" / "metrics" / f"{split_label}_corruption" / "governance_threshold_distribution.csv"
        assert severity_path.exists()
        assert threshold_path.exists()
        with severity_path.open("r", encoding="utf-8", newline="") as handle:
            severity_rows = list(csv.DictReader(handle))
        with threshold_path.open("r", encoding="utf-8", newline="") as handle:
            threshold_rows = list(csv.DictReader(handle))
        assert len(severity_rows) == 2880
        assert len(threshold_rows) == 2880
        assert all("severity_q95" in row for row in severity_rows)
        assert all("theta_q95" in row for row in threshold_rows)
