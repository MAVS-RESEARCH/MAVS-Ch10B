from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


def test_all_systems_share_identical_corrupted_bundle_per_cell() -> None:
    repo_root = Path.cwd()
    for run_id in ("phase3_locked_full_v1", "phase3_audit_full_v1"):
        groups: dict[tuple[str, str, str, str], set[str]] = defaultdict(set)
        with (repo_root / "results" / "stress_runs" / f"{run_id}_prediction_index.csv").open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                key = (row["dataset_id"], row["split"], row["corruption_id"], row["corruption_family"])
                groups[key].add(row["corrupted_input_bundle_hash"])
        assert groups
        assert all(len(values) == 1 for values in groups.values())
