from __future__ import annotations

import csv
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

from mavs_ch10b.verification.hash_utils import console, dependency_versions, git_commit, hash_file, hash_json


def enforce_final_mode_controls(repo_root: Path, config: dict[str, Any]) -> None:
    run_mode = str(config.get("run_mode", "exploratory"))
    import_manifest_path = repo_root / "results" / "baseline_import" / "ch10a_import_manifest.json"
    expected_import_hash = str(config.get("expected_ch10a_import_manifest_sha256", "")).lower()
    actual_import_hash = hash_file(import_manifest_path)
    # Phase 3 console.log: records final-mode import manifest guard evaluation.
    console.log(
        "phase3.run_manifest.import_manifest_guard",
        run_mode=run_mode,
        expected=expected_import_hash,
        actual=actual_import_hash,
        passed=(not expected_import_hash or expected_import_hash == actual_import_hash),
    )
    if expected_import_hash and expected_import_hash != actual_import_hash:
        raise ValueError("Chapter 10A import manifest changed after Phase 1")
    if run_mode != "final":
        return
    if bool(config.get("final_mode_requires_clean_corruption_configs", True)):
        result = subprocess.run(
            ["git", "status", "--porcelain", "--", "configs/corruptions", "results/corruption_manifests"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        dirty = result.stdout.strip()
        # Phase 3 console.log: records final-mode corruption config git cleanliness guard evaluation.
        console.log("phase3.run_manifest.corruption_config_git_guard", dirty=dirty, passed=not dirty)
        if dirty:
            raise ValueError("Final mode refuses uncommitted corruption configs or manifests")


def build_aggregate_rows(prediction_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], dict[str, Any]] = {}
    for record in prediction_records:
        key = (
            record["run_id"],
            record["run_mode"],
            record["split_label"],
            record["split"],
            record["dataset_id"],
            record["system_id"],
            record["corruption_family"],
            record["corruption_level"],
            record["seed_role"],
        )
        if key not in groups:
            groups[key] = {
                "run_id": record["run_id"],
                "run_mode": record["run_mode"],
                "split_label": record["split_label"],
                "split": record["split"],
                "dataset_id": record["dataset_id"],
                "system_id": record["system_id"],
                "corruption_family": record["corruption_family"],
                "corruption_level": record["corruption_level"],
                "seed_role": record["seed_role"],
                "seed_count": 0,
                "system_run_count": 0,
                "prediction_rows": 0,
                "trace_rows": 0,
                "prediction_artifact_count": 0,
            }
        aggregate = groups[key]
        aggregate["seed_count"] += 1
        aggregate["system_run_count"] += 1
        aggregate["prediction_rows"] += int(record["prediction_rows"])
        aggregate["trace_rows"] += int(record.get("trace_rows", 0) or 0)
        aggregate["prediction_artifact_count"] += 1
    for aggregate in groups.values():
        aggregate["aggregate_hash"] = hash_json(aggregate)
    rows = list(groups.values())
    # Phase 3 console.log: records aggregate seed-level index construction.
    console.log("phase3.run_manifest.aggregate_rows_built", rows=len(rows))
    return rows


def write_run_artifacts(
    *,
    repo_root: Path,
    run_id: str,
    config_path: Path,
    config: dict[str, Any],
    command_line: list[str],
    prediction_records: list[dict[str, Any]],
    trace_records: list[dict[str, Any]],
    aggregate_records: list[dict[str, Any]],
) -> dict[str, Any]:
    stress_root = repo_root / str(config["output"]["stress_runs_dir"])
    prediction_index_path = stress_root / f"{run_id}_prediction_index.csv"
    trace_index_path = stress_root / f"{run_id}_trace_index.csv"
    aggregate_index_path = stress_root / f"{run_id}_aggregate_index.csv"
    write_csv(prediction_index_path, prediction_records)
    write_csv(trace_index_path, trace_records)
    write_csv(aggregate_index_path, aggregate_records)
    manifest = {
        "schema_version": "1.0",
        "phase": "phase3",
        "run_id": run_id,
        "run_mode": config.get("run_mode", "exploratory"),
        "experiment_id": config["experiment_id"],
        "split_label": config["split_label"],
        "command_line": command_line,
        "config_path": str(config_path),
        "config_hash": hash_json(config),
        "git_commit": git_commit(repo_root),
        "dependency_versions": dependency_versions(),
        "chapter10a_import_manifest_path": str(repo_root / "results" / "baseline_import" / "ch10a_import_manifest.json"),
        "chapter10a_import_manifest_sha256": hash_file(repo_root / "results" / "baseline_import" / "ch10a_import_manifest.json"),
        "corruption_grid_manifest_path": str(repo_root / "results" / "corruption_manifests" / "corruption_grid_manifest.json"),
        "corruption_grid_manifest_sha256": hash_file(repo_root / "results" / "corruption_manifests" / "corruption_grid_manifest.json"),
        "corruption_manifest_index_path": str(repo_root / "results" / "corruption_manifests" / "corruption_manifest_index.csv"),
        "corruption_manifest_index_sha256": hash_file(repo_root / "results" / "corruption_manifests" / "corruption_manifest_index.csv"),
        "prediction_index_path": str(prediction_index_path),
        "prediction_index_sha256": hash_file(prediction_index_path),
        "trace_index_path": str(trace_index_path),
        "trace_index_sha256": hash_file(trace_index_path),
        "aggregate_index_path": str(aggregate_index_path),
        "aggregate_index_sha256": hash_file(aggregate_index_path),
        "system_run_count": len(prediction_records),
        "governance_trace_artifact_count": len(trace_records),
        "aggregate_row_count": len(aggregate_records),
        "prediction_rows": sum(int(row["prediction_rows"]) for row in prediction_records),
        "trace_rows": sum(int(row["trace_rows"]) for row in trace_records),
        "system_ids": list(config["systems"]),
        "governance_system_ids": list(config["governance_systems"]),
        "run_status": "complete",
    }
    manifest["manifest_payload_sha256"] = hash_json(manifest)
    manifest_path = stress_root / f"{run_id}_run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest["manifest_path"] = str(manifest_path)
    manifest["manifest_file_sha256"] = hash_file(manifest_path)
    # Phase 3 console.log: records Phase 3 run manifest persistence.
    console.log(
        "phase3.run_manifest.written",
        run_id=run_id,
        manifest_path=str(manifest_path),
        system_runs=len(prediction_records),
        trace_rows=manifest["trace_rows"],
    )
    return manifest


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        raise ValueError(f"No records to write: {path}")
    fieldnames = list(records[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    # Phase 3 console.log: records Phase 3 manifest CSV persistence.
    console.log("phase3.run_manifest.csv_written", path=str(path), rows=len(records))
