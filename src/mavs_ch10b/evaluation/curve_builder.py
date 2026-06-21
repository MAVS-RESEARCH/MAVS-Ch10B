from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from mavs_ch10b.evaluation.metrics import METRIC_COLUMNS, write_csv
from mavs_ch10b.evaluation.robustness_area import build_area_rows
from mavs_ch10b.verification.hash_utils import console, hash_file


def build_curve_rows(metric_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in metric_rows:
        key = (row["split_label"], row["dataset_id"], row["system_id"], row["corruption_family"], row["corruption_level"], row["seed_role"])
        groups[key].append(row)
    records: list[dict[str, Any]] = []
    for key, rows in groups.items():
        split_label, dataset_id, system_id, corruption_family, corruption_level, seed_role = key
        record = {
            "split_label": split_label,
            "dataset_id": dataset_id,
            "system_id": system_id,
            "corruption_family": corruption_family,
            "corruption_level": corruption_level,
            "seed_role": seed_role,
            "seed_count": len({row["corruption_seed"] for row in rows}),
            "run_count": len(rows),
        }
        for metric in METRIC_COLUMNS:
            values = [float(row[metric]) for row in rows if row[metric] not in ("", None)]
            record[f"{metric}_mean"] = mean(values) if values else 0.0
            record[f"{metric}_std"] = pstdev(values) if len(values) > 1 else 0.0
        records.append(record)
    # Phase 4 console.log: records robustness curve row construction.
    console.log("phase4.curve_builder.curve_rows_built", rows=len(records))
    return sorted(records, key=lambda row: (row["dataset_id"], row["system_id"], row["corruption_family"], row["split_label"], row["seed_role"], float(row["corruption_level"])))


def write_curve_artifacts(curve_rows: list[dict[str, Any]], output_dir: Path, figure_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in curve_rows:
        grouped[(row["dataset_id"], row["system_id"], row["corruption_family"])].append(row)
    curve_files: list[str] = []
    figure_files: list[str] = []
    for (dataset_id, system_id, corruption_family), rows in grouped.items():
        curve_path = output_dir / f"{dataset_id}__{system_id}__{corruption_family}.csv"
        write_csv(curve_path, rows)
        curve_files.append(str(curve_path))
        figure_path = figure_dir / f"{dataset_id}__{system_id}__{corruption_family}.png"
        write_curve_figure(figure_path, rows, dataset_id, system_id, corruption_family)
        figure_files.append(str(figure_path))
    area_rows = build_area_rows(curve_rows)
    area_path = output_dir / "robustness_curve_area.csv"
    write_csv(area_path, area_rows)
    # Phase 4 console.log: records robustness curve artifact persistence completion.
    console.log("phase4.curve_builder.artifacts_written", curve_files=len(curve_files), figure_files=len(figure_files), area_path=str(area_path))
    return {
        "curve_files": curve_files,
        "figure_files": figure_files,
        "area_path": str(area_path),
        "area_sha256": hash_file(area_path),
        "area_rows": len(area_rows),
    }


def write_curve_figure(path: Path, rows: list[dict[str, Any]], dataset_id: str, system_id: str, corruption_family: str) -> None:
    primary_rows = [row for row in rows if row["seed_role"] in ("primary", "audit")]
    if not primary_rows:
        primary_rows = rows
    fig, ax1 = plt.subplots(figsize=(7, 4), dpi=120)
    labels = sorted({(row["split_label"], row["seed_role"]) for row in primary_rows})
    for split_label, seed_role in labels:
        subset = sorted([row for row in primary_rows if row["split_label"] == split_label and row["seed_role"] == seed_role], key=lambda row: float(row["corruption_level"]))
        if not subset:
            continue
        levels = [float(row["corruption_level"]) for row in subset]
        accuracy = [float(row["accuracy_mean"]) for row in subset]
        unsafe = [float(row["unsafe_acceptance_rate_mean"]) for row in subset]
        ax1.plot(levels, accuracy, marker="o", linewidth=1.5, label=f"{split_label} {seed_role} accuracy")
        ax1.plot(levels, unsafe, marker="x", linewidth=1.0, linestyle="--", label=f"{split_label} {seed_role} unsafe")
    ax1.set_title(f"{dataset_id} | {system_id} | {corruption_family}")
    ax1.set_xlabel("corruption level")
    ax1.set_ylabel("metric value")
    ax1.set_ylim(-0.02, 1.02)
    ax1.grid(True, alpha=0.25)
    ax1.legend(fontsize=6, loc="best")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    # Phase 4 console.log: records robustness curve PNG persistence.
    console.log("phase4.curve_builder.figure_written", path=str(path), sha256=hash_file(path))
