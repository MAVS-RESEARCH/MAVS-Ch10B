from __future__ import annotations

from collections import defaultdict
from typing import Any

import numpy as np

from mavs_ch10b.verification.hash_utils import console, hash_json


AREA_METRICS: dict[str, str] = {
    "accuracy": "higher_is_better",
    "f1": "higher_is_better",
    "unsafe_acceptance_rate": "lower_is_better",
    "technical_failure_rate": "lower_is_better",
    "rejection_rate": "context_dependent",
}


def trapezoid_area(levels: list[float], values: list[float]) -> float:
    if len(levels) != len(values):
        raise ValueError("Levels and values must have equal length")
    if len(levels) < 2:
        return 0.0
    order = np.argsort(np.asarray(levels, dtype=np.float64))
    x = np.asarray(levels, dtype=np.float64)[order]
    y = np.asarray(values, dtype=np.float64)[order]
    return float(np.trapezoid(y, x))


def build_area_rows(curve_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in curve_rows:
        key = (row["split_label"], row["dataset_id"], row["system_id"], row["corruption_family"], row["seed_role"])
        grouped[key].append(row)
    records: list[dict[str, Any]] = []
    for key, rows in grouped.items():
        split_label, dataset_id, system_id, corruption_family, seed_role = key
        levels = [float(row["corruption_level"]) for row in rows]
        for metric, direction in AREA_METRICS.items():
            values = [float(row[f"{metric}_mean"]) for row in rows]
            record = {
                "split_label": split_label,
                "dataset_id": dataset_id,
                "system_id": system_id,
                "corruption_family": corruption_family,
                "seed_role": seed_role,
                "metric": metric,
                "directionality": direction,
                "area": trapezoid_area(levels, values),
                "levels": "|".join(str(level) for level in sorted(levels)),
            }
            record["area_hash"] = hash_json(record)
            records.append(record)
    # Phase 4 console.log: records robustness curve area computation.
    console.log("phase4.robustness_area.rows_built", rows=len(records))
    return records
