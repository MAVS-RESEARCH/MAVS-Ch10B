from __future__ import annotations

from collections import defaultdict
from statistics import mean, pstdev
from typing import Any

from mavs_ch10b.evaluation.metrics import METRIC_COLUMNS
from mavs_ch10b.verification.hash_utils import console, hash_json


def build_system_summary(metric_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in metric_rows:
        key = (row["split_label"], row["dataset_id"], row["system_id"], row["corruption_family"])
        groups[key].append(row)
    records: list[dict[str, Any]] = []
    for key, rows in groups.items():
        split_label, dataset_id, system_id, corruption_family = key
        record = {
            "split_label": split_label,
            "dataset_id": dataset_id,
            "system_id": system_id,
            "corruption_family": corruption_family,
            "run_count": len(rows),
            "evaluated_rows": sum(int(row["evaluated_rows"]) for row in rows),
        }
        for metric in METRIC_COLUMNS:
            if metric == "high_corruption_unsafe_acceptance_rate":
                values = [float(row[metric]) for row in rows if float(row["corruption_level"]) >= 0.8]
            else:
                values = [float(row[metric]) for row in rows if row[metric] not in ("", None)]
            record[f"{metric}_mean"] = mean(values) if values else 0.0
            record[f"{metric}_std"] = pstdev(values) if len(values) > 1 else 0.0
        record["summary_hash"] = hash_json(record)
        records.append(record)
    # Phase 4 console.log: records construction of system-level metric summaries.
    console.log("phase4.aggregation.system_summary_built", rows=len(records))
    return sorted(records, key=lambda row: (row["split_label"], row["dataset_id"], row["system_id"], row["corruption_family"]))


def build_governance_delta_table(metric_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    baselines = ("single_model", "mean_ensemble", "static_weighted_ensemble")
    governance = ("veto_mavs", "pure_mavs_gc")
    indexed = {
        (
            row["split_label"],
            row["dataset_id"],
            row["corruption_id"],
            row["system_id"],
        ): row
        for row in metric_rows
    }
    records: list[dict[str, Any]] = []
    for row in metric_rows:
        if row["system_id"] not in governance:
            continue
        for baseline in baselines:
            base = indexed.get((row["split_label"], row["dataset_id"], row["corruption_id"], baseline))
            if base is None:
                continue
            for metric in ("accuracy", "f1", "unsafe_acceptance_rate", "rejection_rate", "technical_failure_rate"):
                record = {
                    "split_label": row["split_label"],
                    "dataset_id": row["dataset_id"],
                    "corruption_family": row["corruption_family"],
                    "corruption_id": row["corruption_id"],
                    "corruption_level": row["corruption_level"],
                    "corruption_seed": row["corruption_seed"],
                    "seed_role": row["seed_role"],
                    "governance_system_id": row["system_id"],
                    "baseline_system_id": baseline,
                    "metric": metric,
                    "governance_value": row[metric],
                    "baseline_value": base[metric],
                    "delta": float(row[metric]) - float(base[metric]),
                }
                record["delta_hash"] = hash_json(record)
                records.append(record)
    # Phase 4 console.log: records construction of governance-vs-baseline delta table.
    console.log("phase4.aggregation.governance_delta_built", rows=len(records))
    return records
