from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

from mavs_ch10b.evaluation.aggregation import build_system_summary
from mavs_ch10b.evaluation.metrics import compute_prediction_metrics, metric_record, write_csv
from mavs_ch10b.evaluation.safety import conditional_unsafe_acceptance
from mavs_ch10b.verification.hash_utils import console, hash_file, hash_json
from mavs_ch10b.verification.import_audit import validate_no_training_command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Phase 4 robustness metrics from frozen Phase 3 outputs.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--split-label", choices=("locked", "audit", "both"), default="both")
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    validate_no_training_command([Path(sys.argv[0]).name, *sys.argv[1:]])
    split_labels = ("locked", "audit") if args.split_label == "both" else (args.split_label,)
    # Phase 4 console.log: records robustness metric script dispatch.
    console.log("phase4.script.metrics_dispatch", repo_root=str(repo_root), split_labels=list(split_labels))
    manifests = [build_metrics_for_split(repo_root, split_label) for split_label in split_labels]
    # Phase 4 console.log: records robustness metric script completion.
    console.log("phase4.script.metrics_complete", manifests=[manifest["manifest_path"] for manifest in manifests])
    return 0


def build_metrics_for_split(repo_root: Path, split_label: str) -> dict[str, Any]:
    run_id = f"phase3_{split_label}_full_v1"
    prediction_index = repo_root / "results" / "stress_runs" / f"{run_id}_prediction_index.csv"
    trace_index = repo_root / "results" / "stress_runs" / f"{run_id}_trace_index.csv"
    output_dir = repo_root / "results" / "metrics" / f"{split_label}_corruption"
    output_dir.mkdir(parents=True, exist_ok=True)
    # Phase 4 console.log: records split-level metric build dispatch.
    console.log("phase4.metrics.split_start", split_label=split_label, prediction_index=str(prediction_index), trace_index=str(trace_index))
    with prediction_index.open("r", encoding="utf-8", newline="") as handle:
        prediction_rows = list(csv.DictReader(handle))
    trace_by_key = load_trace_index(trace_index)
    metric_rows: list[dict[str, Any]] = []
    severity_rows: list[dict[str, Any]] = []
    threshold_rows: list[dict[str, Any]] = []
    for index, row in enumerate(prediction_rows, start=1):
        metrics, hashes = compute_prediction_metrics(Path(row["prediction_path"]), float(row["corruption_level"]))
        base = {
            "run_id": row["run_id"],
            "run_mode": row["run_mode"],
            "split_label": row["split_label"],
            "split": row["split"],
            "dataset_id": row["dataset_id"],
            "system_id": row["system_id"],
            "corruption_family": row["corruption_family"],
            "corruption_id": row["corruption_id"],
            "corruption_level": row["corruption_level"],
            "corruption_seed": row["corruption_seed"],
            "seed_role": row["seed_role"],
            "corruption_target_space": row["corruption_target_space"],
            "corruption_config_hash": row["corruption_config_hash"],
            "corruption_manifest_hash": row["corruption_manifest_hash"],
            "prediction_path": row["prediction_path"],
            "prediction_sha256": row["prediction_sha256"],
            "trace_required": row["trace_required"],
        }
        trace = trace_by_key.get((row["system_id"], row["corruption_id"]))
        severity_high_unsafe = None
        if trace is not None:
            severity_record, threshold_record, severity_high_unsafe = trace_distribution_records(trace, Path(row["prediction_path"]))
            severity_rows.append({**base, **severity_record})
            threshold_rows.append({**base, **threshold_record})
        metric_rows.append(metric_record({**base, "severity_high_unsafe_acceptance_rate": severity_high_unsafe}, metrics, hashes))
        if index % 1000 == 0:
            # Phase 4 console.log: records metric build progress for large Phase 3 indexes.
            console.log("phase4.metrics.progress", split_label=split_label, processed=index, total=len(prediction_rows))
    metric_path = output_dir / "metric_rows.csv"
    summary_path = output_dir / "system_summary.csv"
    severity_path = output_dir / "governance_severity_distribution.csv"
    threshold_path = output_dir / "governance_threshold_distribution.csv"
    write_csv(metric_path, metric_rows)
    write_csv(summary_path, build_system_summary(metric_rows))
    write_csv(severity_path, severity_rows)
    write_csv(threshold_path, threshold_rows)
    manifest = {
        "schema_version": "1.0",
        "phase": "phase4",
        "split_label": split_label,
        "source_prediction_index": str(prediction_index),
        "source_prediction_index_sha256": hash_file(prediction_index),
        "source_trace_index": str(trace_index),
        "source_trace_index_sha256": hash_file(trace_index),
        "metric_rows": len(metric_rows),
        "severity_rows": len(severity_rows),
        "threshold_rows": len(threshold_rows),
        "metric_rows_path": str(metric_path),
        "metric_rows_sha256": hash_file(metric_path),
        "system_summary_path": str(summary_path),
        "system_summary_sha256": hash_file(summary_path),
        "governance_severity_distribution_path": str(severity_path),
        "governance_severity_distribution_sha256": hash_file(severity_path),
        "governance_threshold_distribution_path": str(threshold_path),
        "governance_threshold_distribution_sha256": hash_file(threshold_path),
        "command_line": [Path(sys.argv[0]).name, *sys.argv[1:]],
    }
    manifest["manifest_payload_sha256"] = hash_json(manifest)
    manifest_path = output_dir / "metric_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest["manifest_path"] = str(manifest_path)
    manifest["manifest_file_sha256"] = hash_file(manifest_path)
    # Phase 4 console.log: records split-level metric build completion.
    console.log("phase4.metrics.split_complete", split_label=split_label, metric_rows=len(metric_rows), severity_rows=len(severity_rows), manifest_path=str(manifest_path))
    return manifest


def load_trace_index(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = {(row["system_id"], row["corruption_id"]): row for row in csv.DictReader(handle)}
    # Phase 4 console.log: records governance trace index loading for metric alignment.
    console.log("phase4.metrics.trace_index_loaded", path=str(path), rows=len(rows))
    return rows


def trace_distribution_records(trace_row: dict[str, str], prediction_path: Path) -> tuple[dict[str, Any], dict[str, Any], float]:
    trace_path = Path(trace_row["trace_path"])
    with np.load(trace_path) as loaded:
        severity = np.asarray(loaded["a"], dtype=np.float64)
        theta = np.asarray(loaded["theta"], dtype=np.float64)
    with np.load(prediction_path) as prediction:
        decisions = np.asarray(prediction["decisions"], dtype=np.int8)
        y_clean = np.asarray(prediction["y_clean"], dtype=np.int8)
    if severity.shape[0] != decisions.shape[0]:
        raise ValueError(f"Trace/prediction row mismatch: {trace_path}")
    severity_record = distribution_record(severity, "severity")
    threshold_record = distribution_record(theta, "theta")
    high_mask = severity >= float(np.quantile(severity, 0.75)) if severity.size else np.asarray([], dtype=bool)
    severity_high_unsafe = conditional_unsafe_acceptance(decisions, y_clean, high_mask)
    # Phase 4 console.log: records governance severity and threshold distribution computation.
    console.log("phase4.metrics.trace_distribution_computed", trace_path=str(trace_path), rows=int(severity.shape[0]), severity_high_unsafe=severity_high_unsafe)
    return severity_record, threshold_record, severity_high_unsafe


def distribution_record(values: np.ndarray, prefix: str) -> dict[str, Any]:
    hist_counts, hist_edges = np.histogram(values, bins=10)
    return {
        f"{prefix}_mean": float(np.mean(values)) if values.size else 0.0,
        f"{prefix}_median": float(np.median(values)) if values.size else 0.0,
        f"{prefix}_min": float(np.min(values)) if values.size else 0.0,
        f"{prefix}_max": float(np.max(values)) if values.size else 0.0,
        f"{prefix}_std": float(np.std(values)) if values.size else 0.0,
        f"{prefix}_q05": float(np.quantile(values, 0.05)) if values.size else 0.0,
        f"{prefix}_q25": float(np.quantile(values, 0.25)) if values.size else 0.0,
        f"{prefix}_q75": float(np.quantile(values, 0.75)) if values.size else 0.0,
        f"{prefix}_q95": float(np.quantile(values, 0.95)) if values.size else 0.0,
        f"{prefix}_hist_counts": "|".join(str(int(value)) for value in hist_counts),
        f"{prefix}_hist_edges": "|".join(f"{float(value):.12g}" for value in hist_edges),
    }


if __name__ == "__main__":
    raise SystemExit(main())
