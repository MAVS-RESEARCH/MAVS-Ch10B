from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from mavs_ch10b.adapters.ch10a_artifacts import CH10A_TRACE_FIELDS
from mavs_ch10b.stress.trace_writer import STRESS_TRACE_FIELDS


def test_governance_trace_rows_align_with_prediction_rows() -> None:
    repo_root = Path.cwd()
    for run_id in ("phase3_locked_full_v1", "phase3_audit_full_v1"):
        with (repo_root / "results" / "stress_runs" / f"{run_id}_prediction_index.csv").open("r", encoding="utf-8", newline="") as handle:
            prediction_rows = {
                (row["system_id"], row["corruption_id"]): int(row["prediction_rows"])
                for row in csv.DictReader(handle)
                if row["system_id"] in {"veto_mavs", "pure_mavs_gc"}
            }
        with (repo_root / "results" / "stress_runs" / f"{run_id}_trace_index.csv").open("r", encoding="utf-8", newline="") as handle:
            trace_rows = list(csv.DictReader(handle))
        assert trace_rows
        for row in trace_rows:
            assert int(row["trace_rows"]) == prediction_rows[(row["system_id"], row["corruption_id"])]


def test_sample_governance_trace_contains_required_fields() -> None:
    repo_root = Path.cwd()
    run_id = "phase3_locked_full_v1"
    with (repo_root / "results" / "stress_runs" / f"{run_id}_trace_index.csv").open("r", encoding="utf-8", newline="") as handle:
        first = next(csv.DictReader(handle))
    with np.load(first["trace_path"]) as loaded:
        payload = json.loads(str(loaded["metadata_json"]))
    for field in CH10A_TRACE_FIELDS:
        assert field in payload["fields"]
    for field in STRESS_TRACE_FIELDS:
        assert field in payload["fields"]
    assert payload["specialist_ids"] == ["random_forest", "gradient_boosted_trees", "mlp"]
    assert payload["format"] == "columnar_npz"
