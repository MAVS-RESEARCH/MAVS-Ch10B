from __future__ import annotations

import csv
import json
from pathlib import Path


def test_locked_and_audit_stress_matrix_manifests_are_complete() -> None:
    repo_root = Path.cwd()
    for run_id, expected_system_runs, expected_trace_artifacts in (
        ("phase3_locked_full_v1", 7200, 2880),
        ("phase3_audit_full_v1", 7200, 2880),
    ):
        manifest_path = repo_root / "results" / "stress_runs" / f"{run_id}_run_manifest.json"
        assert manifest_path.exists(), run_id
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["run_status"] == "complete"
        assert manifest["system_run_count"] == expected_system_runs
        assert manifest["governance_trace_artifact_count"] == expected_trace_artifacts
        assert manifest["prediction_rows"] > 0
        assert manifest["trace_rows"] > 0
        assert Path(manifest["prediction_index_path"]).exists()
        assert Path(manifest["trace_index_path"]).exists()
        assert Path(manifest["aggregate_index_path"]).exists()


def test_prediction_index_has_every_required_system_family_and_level() -> None:
    repo_root = Path.cwd()
    expected_systems = {"single_model", "mean_ensemble", "static_weighted_ensemble", "veto_mavs", "pure_mavs_gc"}
    expected_families = {
        "feature_noise",
        "missing_features",
        "random_feature_deletion",
        "label_noise",
        "confidence_distortion",
        "adversarial_confidence_inflation",
        "distribution_shift",
        "synthetic_sensor_failure",
        "specialist_failure",
    }
    expected_levels = {"0.0", "0.05", "0.1", "0.2", "0.4", "0.6", "0.8", "1.0"}
    for run_id in ("phase3_locked_full_v1", "phase3_audit_full_v1"):
        with (repo_root / "results" / "stress_runs" / f"{run_id}_prediction_index.csv").open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        assert {row["system_id"] for row in rows} == expected_systems
        assert {row["corruption_family"] for row in rows} == expected_families
        assert {row["corruption_level"] for row in rows} == expected_levels
