from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any

import numpy as np

from mavs_ch10b.verification.hash_utils import console, hash_json


def build_seed_level_variance(metric_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[float]] = defaultdict(list)
    for row in metric_rows:
        key = (row["split_label"], row["dataset_id"], row["system_id"], row["corruption_family"], row["corruption_level"], row["seed_role"])
        groups[key].append(float(row["accuracy"]))
    records: list[dict[str, Any]] = []
    for key, values in groups.items():
        split_label, dataset_id, system_id, corruption_family, corruption_level, seed_role = key
        record = {
            "split_label": split_label,
            "dataset_id": dataset_id,
            "system_id": system_id,
            "corruption_family": corruption_family,
            "corruption_level": corruption_level,
            "seed_role": seed_role,
            "seed_count": len(values),
            "accuracy_mean": mean(values) if values else 0.0,
            "accuracy_variance": float(np.var(values)) if values else 0.0,
        }
        record["variance_hash"] = hash_json(record)
        records.append(record)
    # Phase 4 console.log: records seed-level variance table construction.
    console.log("phase4.statistics.seed_variance_built", rows=len(records))
    return records


def build_seed_level_bootstrap_cis(metric_rows: list[dict[str, Any]], *, iterations: int = 500, seed: int = 4040) -> list[dict[str, Any]]:
    baselines = ("single_model", "mean_ensemble", "static_weighted_ensemble")
    governance = ("veto_mavs", "pure_mavs_gc")
    indexed = {
        (
            row["split_label"],
            row["dataset_id"],
            row["corruption_family"],
            row["corruption_level"],
            row["seed_role"],
            row["corruption_seed"],
            row["system_id"],
        ): row
        for row in metric_rows
    }
    groups: dict[tuple[Any, ...], list[str]] = defaultdict(list)
    for row in metric_rows:
        if row["system_id"] in governance:
            key = (row["split_label"], row["dataset_id"], row["corruption_family"], row["corruption_level"], row["seed_role"], row["system_id"])
            groups[key].append(row["corruption_seed"])
    rng = np.random.default_rng(seed)
    records: list[dict[str, Any]] = []
    for key, seeds in groups.items():
        split_label, dataset_id, corruption_family, corruption_level, seed_role, gov_system = key
        unique_seeds = sorted(set(seeds))
        if len(unique_seeds) < 2:
            continue
        for baseline in baselines:
            for metric in ("accuracy", "f1", "unsafe_acceptance_rate"):
                deltas: list[float] = []
                for corruption_seed in unique_seeds:
                    gov = indexed.get((split_label, dataset_id, corruption_family, corruption_level, seed_role, corruption_seed, gov_system))
                    base = indexed.get((split_label, dataset_id, corruption_family, corruption_level, seed_role, corruption_seed, baseline))
                    if gov is None or base is None:
                        continue
                    deltas.append(float(gov[metric]) - float(base[metric]))
                if len(deltas) < 2:
                    continue
                samples = np.asarray(deltas, dtype=np.float64)
                boot = rng.choice(samples, size=(iterations, samples.shape[0]), replace=True).mean(axis=1)
                record = {
                    "split_label": split_label,
                    "dataset_id": dataset_id,
                    "corruption_family": corruption_family,
                    "corruption_level": corruption_level,
                    "seed_role": seed_role,
                    "governance_system_id": gov_system,
                    "baseline_system_id": baseline,
                    "metric": metric,
                    "bootstrap_unit": "seed_level_paired_by_corruption_seed",
                    "seed_count": len(samples),
                    "delta_mean": float(np.mean(samples)),
                    "ci_lower": float(np.quantile(boot, 0.025)),
                    "ci_upper": float(np.quantile(boot, 0.975)),
                    "iterations": iterations,
                    "bootstrap_seed": seed,
                }
                record["bootstrap_hash"] = hash_json(record)
                records.append(record)
    # Phase 4 console.log: records paired bootstrap CI table construction.
    console.log("phase4.statistics.bootstrap_cis_built", rows=len(records), iterations=iterations)
    return records
