from __future__ import annotations

import csv
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

from mavs_ch10b.adapters.ch10a_artifacts import BENCHMARK_SPLITS, REQUIRED_DATASET_IDS, REQUIRED_SYSTEM_IDS
from mavs_ch10b.adapters.ch10a_source import locate_ch10a_source
from mavs_ch10b.adapters.ch10a_systems import build_comparison_systems, load_frozen_manifest, load_specialist_bundle, run_system
from mavs_ch10b.verification.hash_utils import console, dependency_versions, git_commit, hash_file, hash_json, write_json
from mavs_ch10b.verification.import_audit import validate_no_training_command


METRIC_NAMES: tuple[str, ...] = (
    "accuracy",
    "precision",
    "recall",
    "f1",
    "roc_auc",
    "false_positive_rate",
    "false_negative_rate",
    "balanced_accuracy",
    "calibration_error",
)


def run_clean_baseline(repo_root: Path, config_path: Path, tolerance: float | None = None) -> dict[str, Any]:
    validate_no_training_command(["run_clean_baseline.py"])
    source = locate_ch10a_source(repo_root, config_path)
    output_dir = repo_root / "results" / "baseline_import"
    output_dir.mkdir(parents=True, exist_ok=True)
    tolerance_value = float(tolerance if tolerance is not None else source.config.get("baseline_tolerance", 1e-12))
    # Phase 1 console.log: records clean baseline replay dispatch.
    console.log("phase1.baseline_runner.dispatch", ch10a_root=str(source.repo_root), output_dir=str(output_dir), tolerance=tolerance_value)

    frozen_manifest = load_frozen_manifest(source)
    metrics_records: list[dict[str, Any]] = []
    for split_label, split_name in BENCHMARK_SPLITS.items():
        # Phase 1 console.log: records clean replay split start.
        console.log("phase1.baseline_runner.split_start", split_label=split_label, split=split_name)
        for dataset_id in REQUIRED_DATASET_IDS:
            bundle = load_specialist_bundle(source, dataset_id, split_name)
            systems = build_comparison_systems(source, dataset_id, frozen_manifest)
            for system in systems:
                output = run_system(system, bundle)
                metrics = compute_metrics_with_ch10a(source, output)
                record = {
                    "benchmark_id": split_label,
                    "split": split_name,
                    "dataset_id": dataset_id,
                    "system_id": output.system_id,
                    **{name: metrics[name] for name in METRIC_NAMES},
                    "rows": metrics["rows"],
                    "positives": metrics["positives"],
                    "predicted_positives": metrics["predicted_positives"],
                    "true_positive": metrics["confusion"]["true_positive"],
                    "false_positive": metrics["confusion"]["false_positive"],
                    "true_negative": metrics["confusion"]["true_negative"],
                    "false_negative": metrics["confusion"]["false_negative"],
                    "trace_rows": output.trace_rows,
                }
                metrics_records.append(record)
                # Phase 1 console.log: records clean replay metric computation for one system.
                console.log(
                    "phase1.baseline_runner.system_metrics_computed",
                    dataset_id=dataset_id,
                    split=split_name,
                    system_id=output.system_id,
                    accuracy=record["accuracy"],
                    f1=record["f1"],
                    trace_rows=output.trace_rows,
                )

    metrics_path = output_dir / "clean_replay_metrics.csv"
    write_csv(metrics_path, metrics_records)
    comparison_records = compare_against_ch10a(source.repo_root, metrics_records, tolerance_value)
    comparison_path = output_dir / "clean_replay_comparison.csv"
    write_csv(comparison_path, comparison_records)
    failures = [row for row in comparison_records if row["status"] != "pass"]
    report_path = output_dir / "clean_replay_compatibility_report.md"
    write_compatibility_report(report_path, comparison_records, failures, tolerance_value)
    manifest_path = output_dir / "clean_replay_manifest.json"
    manifest = {
        "schema_version": "1.0",
        "phase": "phase1",
        "ch10a_root": str(source.repo_root),
        "ch10a_current_git_commit": git_commit(source.repo_root),
        "ch10b_git_commit": git_commit(repo_root),
        "dependency_versions": dependency_versions(),
        "datasets": list(REQUIRED_DATASET_IDS),
        "systems": list(REQUIRED_SYSTEM_IDS),
        "splits": BENCHMARK_SPLITS,
        "tolerance": tolerance_value,
        "metric_rows": len(metrics_records),
        "comparison_rows": len(comparison_records),
        "comparison_failures": len(failures),
        "artifacts": {
            "clean_replay_metrics": str(metrics_path),
            "clean_replay_metrics_sha256": hash_file(metrics_path),
            "clean_replay_comparison": str(comparison_path),
            "clean_replay_comparison_sha256": hash_file(comparison_path),
            "clean_replay_compatibility_report": str(report_path),
            "clean_replay_compatibility_report_sha256": hash_file(report_path),
        },
    }
    manifest["manifest_payload_sha256"] = hash_json(manifest)
    write_json(manifest_path, manifest)
    manifest["manifest_file_sha256"] = hash_file(manifest_path)
    # Phase 1 console.log: records clean baseline replay completion.
    console.log(
        "phase1.baseline_runner.complete",
        metrics_path=str(metrics_path),
        comparison_path=str(comparison_path),
        manifest_path=str(manifest_path),
        comparison_failures=len(failures),
    )
    if failures:
        raise ValueError(f"Clean replay compatibility failed for {len(failures)} metric cells")
    return manifest


def compute_metrics_with_ch10a(source: Any, output: Any) -> dict[str, Any]:
    from mavs_ch10b.adapters.ch10a_source import ensure_ch10a_importable

    ensure_ch10a_importable(source)
    from mavs_ch10a.evaluation.metrics import compute_binary_metrics

    metrics = compute_binary_metrics(output.labels, output.probabilities, output.decisions, emit_console=False)
    # Phase 1 console.log: records Chapter 10A metric function use during clean replay.
    console.log("phase1.baseline_runner.ch10a_metrics_computed", rows=metrics["rows"], accuracy=metrics["accuracy"])
    return metrics


def compare_against_ch10a(ch10a_root: Path, records: list[dict[str, Any]], tolerance: float) -> list[dict[str, Any]]:
    source_rows = load_source_metric_rows(ch10a_root)
    comparison_records: list[dict[str, Any]] = []
    for record in records:
        key = (record["benchmark_id"], record["dataset_id"], record["system_id"])
        if key not in source_rows:
            raise KeyError(f"Missing Chapter 10A source metric row: {key}")
        source_row = source_rows[key]
        for metric in METRIC_NAMES:
            replay_value = float(record[metric])
            source_value = float(source_row[metric])
            if np.isnan(replay_value) and np.isnan(source_value):
                delta = 0.0
            else:
                delta = abs(replay_value - source_value)
            comparison_records.append(
                {
                    "benchmark_id": record["benchmark_id"],
                    "split": record["split"],
                    "dataset_id": record["dataset_id"],
                    "system_id": record["system_id"],
                    "metric": metric,
                    "replay_value": replay_value,
                    "chapter10a_value": source_value,
                    "absolute_delta": delta,
                    "tolerance": tolerance,
                    "status": "pass" if delta <= tolerance else "fail",
                }
            )
    # Phase 1 console.log: records clean replay compatibility comparison construction.
    console.log("phase1.baseline_runner.comparison_built", rows=len(comparison_records), tolerance=tolerance)
    return comparison_records


def load_source_metric_rows(ch10a_root: Path) -> dict[tuple[str, str, str], dict[str, str]]:
    rows: dict[tuple[str, str, str], dict[str, str]] = {}
    for split_label in ("locked", "audit"):
        path = ch10a_root / "results" / "metrics" / split_label / "benchmark_metrics_summary.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                rows[(row["benchmark_id"], row["dataset_id"], row["system_id"])] = row
        # Phase 1 console.log: records Chapter 10A source metric summary loading.
        console.log("phase1.baseline_runner.source_metrics_loaded", split_label=split_label, path=str(path))
    return rows


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    if not records:
        raise ValueError(f"No records to write: {path}")
    fieldnames = list(records[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    # Phase 1 console.log: records CSV artifact persistence.
    console.log("phase1.baseline_runner.csv_written", path=str(path), rows=len(records))


def write_compatibility_report(path: Path, comparisons: list[dict[str, Any]], failures: list[dict[str, Any]], tolerance: float) -> None:
    lines = [
        "# Chapter 10B Phase 1 Clean Replay Compatibility Report",
        "",
        f"Tolerance: `{tolerance}`",
        f"Comparison rows: `{len(comparisons)}`",
        f"Failures: `{len(failures)}`",
        "",
        "## Result",
        "",
        "Clean replay compatibility status: `pass`." if not failures else "Clean replay compatibility status: `fail`.",
    ]
    if failures:
        lines.extend(["", "## Failing Rows", "", "| Dataset | Split | System | Metric | Delta |", "| --- | --- | --- | --- | ---: |"])
        for failure in failures:
            lines.append(
                f"| {failure['dataset_id']} | {failure['split']} | {failure['system_id']} | {failure['metric']} | {failure['absolute_delta']} |"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # Phase 1 console.log: records clean replay compatibility report persistence.
    console.log("phase1.baseline_runner.compatibility_report_written", path=str(path), failures=len(failures))

