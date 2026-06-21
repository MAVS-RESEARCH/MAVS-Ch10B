from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

import pandas as pd

from mavs_ch10b.verification.hash_utils import console, hash_file, hash_json


REPORT_METRICS: tuple[str, ...] = (
    "accuracy",
    "f1",
    "unsafe_acceptance_rate",
    "technical_failure_rate",
    "rejection_rate",
    "high_corruption_unsafe_acceptance_rate",
)

DELTA_METRICS: tuple[str, ...] = (
    "accuracy",
    "f1",
    "unsafe_acceptance_rate",
    "rejection_rate",
    "technical_failure_rate",
)

DIRECTIONALITY: dict[str, str] = {
    "accuracy": "higher_is_better",
    "f1": "higher_is_better",
    "unsafe_acceptance_rate": "lower_is_better",
    "technical_failure_rate": "lower_is_better",
    "high_corruption_unsafe_acceptance_rate": "lower_is_better",
    "rejection_rate": "context_dependent",
}

SYSTEM_NAMES: dict[str, str] = {
    "single_model": "Single Best Model",
    "mean_ensemble": "Mean Ensemble",
    "static_weighted_ensemble": "Static Weighted Ensemble",
    "veto_mavs": "Veto MAVS",
    "pure_mavs_gc": "Pure MAVS-GC",
}


def read_csv(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    # Phase 5 console.log: records CSV input loading for report table construction.
    console.log("phase5.tables.csv_loaded", path=str(path), rows=int(frame.shape[0]))
    return frame


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, lineterminator="\n")
    # Phase 5 console.log: records CSV report artifact persistence.
    console.log("phase5.tables.csv_written", path=str(path), rows=int(frame.shape[0]), sha256=hash_file(path))


def load_metric_rows(repo_root: Path) -> pd.DataFrame:
    frames = []
    for split_label in ("locked", "audit"):
        frames.append(read_csv(repo_root / "results" / "metrics" / f"{split_label}_corruption" / "metric_rows.csv"))
    frame = pd.concat(frames, ignore_index=True)
    # Phase 5 console.log: records combined metric row loading across locked and audit splits.
    console.log("phase5.tables.metric_rows_loaded", rows=int(frame.shape[0]), splits=sorted(frame["split_label"].unique().tolist()))
    return frame


def load_area_rows(repo_root: Path) -> pd.DataFrame:
    frame = read_csv(repo_root / "results" / "robustness_curves" / "robustness_curve_area.csv")
    # Phase 5 console.log: records robustness area row loading for report construction.
    console.log("phase5.tables.area_rows_loaded", rows=int(frame.shape[0]))
    return frame


def load_governance_distributions(repo_root: Path, name: str) -> pd.DataFrame:
    frames = []
    for split_label in ("locked", "audit"):
        frames.append(read_csv(repo_root / "results" / "metrics" / f"{split_label}_corruption" / name))
    frame = pd.concat(frames, ignore_index=True)
    # Phase 5 console.log: records governance distribution loading for report construction.
    console.log("phase5.tables.governance_distribution_loaded", name=name, rows=int(frame.shape[0]))
    return frame


def build_robustness_table(repo_root: Path, metric_rows: pd.DataFrame, area_rows: pd.DataFrame) -> pd.DataFrame:
    metric_records = []
    source_paths = {
        split: str(repo_root / "results" / "metrics" / f"{split}_corruption" / "metric_rows.csv")
        for split in ("locked", "audit")
    }
    source_hashes = {split: hash_file(Path(path)) for split, path in source_paths.items()}
    metric_base = [
        "split_label",
        "split",
        "dataset_id",
        "system_id",
        "corruption_family",
        "corruption_level",
        "corruption_seed",
        "seed_role",
        "run_mode",
        "corruption_target_space",
    ]
    for metric in REPORT_METRICS:
        for row in metric_rows.itertuples(index=False):
            payload = {column: getattr(row, column) for column in metric_base}
            payload.update(
                {
                    "table_type": "metric",
                    "metric": metric,
                    "value": float(getattr(row, metric)),
                    "directionality": DIRECTIONALITY[metric],
                    "locked_value": "",
                    "audit_value": "",
                    "delta": "",
                    "absolute_delta": "",
                    "source_artifact": source_paths[row.split_label],
                    "source_artifact_sha256": source_hashes[row.split_label],
                    "source_row_hash": getattr(row, "metric_row_hash"),
                }
            )
            payload["evidence_hash"] = hash_json(payload)
            metric_records.append(payload)
    metric_frame = pd.DataFrame(metric_records)
    area_frame = _area_comparison_frame(repo_root, area_rows)
    consistency_frame = build_locked_audit_consistency(repo_root, area_rows)
    combined = pd.concat([metric_frame, area_frame, consistency_frame], ignore_index=True, sort=False).fillna("")
    column_order = [
        "table_type",
        "split_label",
        "split",
        "dataset_id",
        "system_id",
        "corruption_family",
        "corruption_level",
        "corruption_seed",
        "seed_role",
        "run_mode",
        "corruption_target_space",
        "metric",
        "value",
        "directionality",
        "locked_value",
        "audit_value",
        "delta",
        "absolute_delta",
        "source_artifact",
        "source_artifact_sha256",
        "source_row_hash",
        "evidence_hash",
    ]
    combined = combined.reindex(columns=column_order)
    # Phase 5 console.log: records long-form robustness table construction.
    console.log("phase5.tables.robustness_table_built", rows=int(combined.shape[0]), metric_rows=len(metric_records), area_rows=int(area_frame.shape[0]), consistency_rows=int(consistency_frame.shape[0]))
    return combined


def build_locked_audit_consistency(repo_root: Path, area_rows: pd.DataFrame) -> pd.DataFrame:
    source_path = repo_root / "results" / "robustness_curves" / "robustness_curve_area.csv"
    grouped = (
        area_rows.groupby(["split_label", "dataset_id", "system_id", "corruption_family", "metric", "directionality"], as_index=False)["area"]
        .mean()
        .rename(columns={"area": "area_mean"})
    )
    locked = grouped[grouped["split_label"] == "locked"].drop(columns=["split_label"]).rename(columns={"area_mean": "locked_value"})
    audit = grouped[grouped["split_label"] == "audit"].drop(columns=["split_label"]).rename(columns={"area_mean": "audit_value"})
    merged = locked.merge(audit, on=["dataset_id", "system_id", "corruption_family", "metric", "directionality"], how="inner")
    merged["table_type"] = "locked_audit_area_consistency"
    merged["split_label"] = "locked_vs_audit"
    merged["split"] = "locked_benchmark_vs_audit_benchmark"
    merged["corruption_level"] = ""
    merged["corruption_seed"] = ""
    merged["seed_role"] = ""
    merged["run_mode"] = "exploratory"
    merged["corruption_target_space"] = ""
    merged["value"] = ""
    merged["delta"] = merged["audit_value"] - merged["locked_value"]
    merged["absolute_delta"] = merged["delta"].abs()
    merged["source_artifact"] = str(source_path)
    merged["source_artifact_sha256"] = hash_file(source_path)
    merged["source_row_hash"] = ""
    merged["evidence_hash"] = merged.apply(lambda row: hash_json(row.to_dict()), axis=1)
    # Phase 5 console.log: records locked-vs-audit consistency table construction.
    console.log("phase5.tables.locked_audit_consistency_built", rows=int(merged.shape[0]))
    return merged


def build_system_delta_table(metric_rows: pd.DataFrame) -> pd.DataFrame:
    merge_keys = ["split_label", "dataset_id", "corruption_id"]
    records = []
    comparisons = {
        "veto_mavs": ("single_model", "mean_ensemble", "static_weighted_ensemble"),
        "pure_mavs_gc": ("single_model", "mean_ensemble", "static_weighted_ensemble", "veto_mavs"),
    }
    for subject_system, baselines in comparisons.items():
        subject = metric_rows[metric_rows["system_id"] == subject_system]
        for baseline_system in baselines:
            baseline = metric_rows[metric_rows["system_id"] == baseline_system]
            merged = subject.merge(baseline, on=merge_keys, suffixes=("_subject", "_baseline"))
            for metric in DELTA_METRICS:
                for row in merged.itertuples(index=False):
                    subject_value = float(getattr(row, f"{metric}_subject"))
                    baseline_value = float(getattr(row, f"{metric}_baseline"))
                    delta = subject_value - baseline_value
                    payload = {
                        "split_label": row.split_label,
                        "dataset_id": row.dataset_id,
                        "corruption_family": row.corruption_family_subject,
                        "corruption_id": row.corruption_id,
                        "corruption_level": row.corruption_level_subject,
                        "corruption_seed": row.corruption_seed_subject,
                        "seed_role": row.seed_role_subject,
                        "subject_system_id": subject_system,
                        "baseline_system_id": baseline_system,
                        "metric": metric,
                        "directionality": DIRECTIONALITY[metric],
                        "subject_value": subject_value,
                        "baseline_value": baseline_value,
                        "delta": delta,
                        "interpretation": interpret_delta(metric, delta),
                    }
                    payload["system_delta_hash"] = hash_json(payload)
                    records.append(payload)
    frame = pd.DataFrame(records)
    # Phase 5 console.log: records expanded governance system delta table construction.
    console.log("phase5.tables.system_delta_table_built", rows=int(frame.shape[0]), comparisons=sum(len(value) for value in comparisons.values()))
    return frame


def interpret_delta(metric: str, delta: float) -> str:
    if abs(delta) < 1e-12:
        return "neutral"
    directionality = DIRECTIONALITY[metric]
    if directionality == "higher_is_better":
        return "improved" if delta > 0.0 else "worse"
    if directionality == "lower_is_better":
        return "improved" if delta < 0.0 else "worse"
    return "higher_rejection" if delta > 0.0 else "lower_rejection"


def build_summary_statistics(metric_rows: pd.DataFrame, area_rows: pd.DataFrame, system_deltas: pd.DataFrame, severity_rows: pd.DataFrame, threshold_rows: pd.DataFrame) -> dict[str, Any]:
    overall = _records(
        metric_rows.groupby("system_id", as_index=False)[["accuracy", "f1", "unsafe_acceptance_rate", "rejection_rate", "technical_failure_rate"]]
        .mean()
        .sort_values("accuracy", ascending=False)
    )
    high_corruption = _records(
        metric_rows[metric_rows["corruption_level"] >= 0.8]
        .groupby("system_id", as_index=False)[["accuracy", "f1", "unsafe_acceptance_rate", "rejection_rate"]]
        .mean()
        .sort_values("unsafe_acceptance_rate")
    )
    area_summary = _records(
        area_rows.groupby(["system_id", "metric", "directionality"], as_index=False)["area"].mean().sort_values(["metric", "area"])
    )
    family_damage = _records(
        metric_rows.groupby("corruption_family", as_index=False)[["accuracy", "f1", "unsafe_acceptance_rate", "rejection_rate"]]
        .mean()
        .sort_values("accuracy")
    )
    delta_summary = _records(
        system_deltas.groupby(["subject_system_id", "baseline_system_id", "metric", "directionality"], as_index=False)["delta"]
        .mean()
        .sort_values(["subject_system_id", "baseline_system_id", "metric"])
    )
    severity_summary = _records(severity_rows.groupby("system_id", as_index=False)[["severity_mean", "severity_q95"]].mean())
    threshold_summary = _records(threshold_rows.groupby("system_id", as_index=False)[["theta_mean", "theta_q95"]].mean())
    worst_rows = _records(
        metric_rows.sort_values(["accuracy", "unsafe_acceptance_rate"], ascending=[True, False])
        .head(20)[["split_label", "dataset_id", "system_id", "corruption_family", "corruption_level", "seed_role", "corruption_seed", "accuracy", "f1", "unsafe_acceptance_rate", "rejection_rate"]]
    )
    summary = {
        "run_modes": sorted(metric_rows["run_mode"].unique().tolist()),
        "datasets": sorted(metric_rows["dataset_id"].unique().tolist()),
        "splits": sorted(metric_rows["split_label"].unique().tolist()),
        "systems": sorted(metric_rows["system_id"].unique().tolist()),
        "corruption_families": sorted(metric_rows["corruption_family"].unique().tolist()),
        "levels": sorted(float(value) for value in metric_rows["corruption_level"].unique().tolist()),
        "metric_rows": int(metric_rows.shape[0]),
        "area_rows": int(area_rows.shape[0]),
        "system_delta_rows": int(system_deltas.shape[0]),
        "overall_system_means": overall,
        "high_corruption_system_means": high_corruption,
        "area_summary": area_summary,
        "family_damage": family_damage,
        "delta_summary": delta_summary,
        "severity_summary": severity_summary,
        "threshold_summary": threshold_summary,
        "worst_rows": worst_rows,
    }
    # Phase 5 console.log: records report summary statistic construction.
    console.log("phase5.tables.summary_statistics_built", metric_rows=summary["metric_rows"], area_rows=summary["area_rows"], system_delta_rows=summary["system_delta_rows"])
    return summary


def _area_comparison_frame(repo_root: Path, area_rows: pd.DataFrame) -> pd.DataFrame:
    source_path = repo_root / "results" / "robustness_curves" / "robustness_curve_area.csv"
    frame = area_rows.copy()
    frame["table_type"] = "robustness_area"
    frame["split"] = frame["split_label"].map({"locked": "locked_benchmark", "audit": "audit_benchmark"}).fillna(frame["split_label"])
    frame["corruption_level"] = ""
    frame["corruption_seed"] = ""
    frame["run_mode"] = "exploratory"
    frame["corruption_target_space"] = ""
    frame["value"] = frame["area"]
    frame["locked_value"] = ""
    frame["audit_value"] = ""
    frame["delta"] = ""
    frame["absolute_delta"] = ""
    frame["source_artifact"] = str(source_path)
    frame["source_artifact_sha256"] = hash_file(source_path)
    frame["source_row_hash"] = frame["area_hash"]
    frame["evidence_hash"] = frame.apply(lambda row: hash_json(row.to_dict()), axis=1)
    return frame


def _records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    normalized = frame.copy()
    for column in normalized.columns:
        if pd.api.types.is_float_dtype(normalized[column]):
            normalized[column] = normalized[column].astype(float)
    return normalized.to_dict(orient="records")


def mean_for(records: Iterable[dict[str, Any]], key: str) -> float:
    values = [float(record[key]) for record in records]
    return sum(values) / len(values) if values else 0.0
