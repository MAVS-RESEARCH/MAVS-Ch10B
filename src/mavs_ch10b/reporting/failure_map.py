from __future__ import annotations

from pathlib import Path

import pandas as pd

from mavs_ch10b.reporting.corruption_atlas import FAILURE_CLASS
from mavs_ch10b.reporting.tables import SYSTEM_NAMES
from mavs_ch10b.verification.hash_utils import console, hash_file


def build_failure_map(repo_root: Path, metric_rows: pd.DataFrame, system_deltas: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or repo_root / "results" / "reports" / "failure_map.md"
    family_damage = metric_rows.groupby("corruption_family", as_index=False)[["accuracy", "f1", "unsafe_acceptance_rate", "rejection_rate"]].mean().sort_values("accuracy")
    pure_vs_veto = system_deltas[(system_deltas["subject_system_id"] == "pure_mavs_gc") & (system_deltas["baseline_system_id"] == "veto_mavs")]
    veto_vs_mean = system_deltas[(system_deltas["subject_system_id"] == "veto_mavs") & (system_deltas["baseline_system_id"] == "mean_ensemble")]
    pure_worst = metric_rows[metric_rows["system_id"] == "pure_mavs_gc"].sort_values(["accuracy", "rejection_rate"], ascending=[True, False]).head(8)
    veto_unsafe = metric_rows[metric_rows["system_id"] == "veto_mavs"].sort_values("unsafe_acceptance_rate", ascending=False).head(8)
    governance_rows = metric_rows[metric_rows["system_id"].isin(["veto_mavs", "pure_mavs_gc"])]
    surviving_unsafe = governance_rows[governance_rows["unsafe_acceptance_rate"] > 0.1].sort_values("unsafe_acceptance_rate", ascending=False).head(12)
    over_rejection = governance_rows[governance_rows["rejection_rate"] >= 0.95].sort_values(["rejection_rate", "accuracy"], ascending=[False, True]).head(12)
    under_rejection = governance_rows[(governance_rows["unsafe_acceptance_rate"] >= 0.5) & (governance_rows["rejection_rate"] <= 0.1)].sort_values("unsafe_acceptance_rate", ascending=False).head(12)
    lines = [
        "# Failure Map",
        "",
        "This map identifies where MAVS governance fails, where it suppresses unsafe acceptance, and where it shifts errors into rejection. All evidence is from locked and audit Phase 4 metric artifacts.",
        "",
        "## Executive Failure Summary",
        "",
        f"- Most damaging corruption family by mean accuracy: `{family_damage.iloc[0]['corruption_family']}` with mean accuracy `{float(family_damage.iloc[0]['accuracy']):.6f}`.",
        f"- Pure MAVS-GC vs Veto MAVS average accuracy delta: `{_mean_delta(pure_vs_veto, 'accuracy'):.6f}`.",
        f"- Pure MAVS-GC vs Veto MAVS average unsafe acceptance delta: `{_mean_delta(pure_vs_veto, 'unsafe_acceptance_rate'):.6f}`.",
        f"- Pure MAVS-GC vs Veto MAVS average rejection-rate delta: `{_mean_delta(pure_vs_veto, 'rejection_rate'):.6f}`.",
        f"- Veto MAVS vs Mean Ensemble average accuracy delta: `{_mean_delta(veto_vs_mean, 'accuracy'):.6f}`.",
        f"- Veto MAVS vs Mean Ensemble average unsafe acceptance delta: `{_mean_delta(veto_vs_mean, 'unsafe_acceptance_rate'):.6f}`.",
        "",
        "## When Pure MAVS-GC Fails",
        "",
        "Pure MAVS-GC fails primarily by over-rejection in the observed artifacts. Its lowest-accuracy rows often have `rejection_rate = 1.0`, which suppresses unsafe acceptance but can destroy F1.",
        "",
        _markdown_table(pure_worst, ["split_label", "dataset_id", "corruption_family", "corruption_level", "seed_role", "corruption_seed", "accuracy", "f1", "unsafe_acceptance_rate", "rejection_rate"]),
        "",
        "## When Veto MAVS Fails",
        "",
        "Veto MAVS fails when the veto control does not change the mean-ensemble decision stream. In the generated deltas, Veto MAVS and Mean Ensemble have zero average delta for the primary metrics.",
        "",
        _markdown_table(veto_unsafe, ["split_label", "dataset_id", "corruption_family", "corruption_level", "seed_role", "corruption_seed", "accuracy", "f1", "unsafe_acceptance_rate", "rejection_rate"]),
        "",
        "## Governance Over-Rejection",
        "",
        "Over-rejection is recorded where governance systems reject at least 95 percent of evaluated rows. This is a safety tradeoff, not a free robustness improvement.",
        "",
        _markdown_table(over_rejection, ["split_label", "dataset_id", "system_id", "corruption_family", "corruption_level", "seed_role", "corruption_seed", "accuracy", "f1", "unsafe_acceptance_rate", "rejection_rate"]),
        "",
        "## Governance Under-Rejection",
        "",
        "Under-rejection is recorded where unsafe acceptance is at least 50 percent while rejection is at most 10 percent.",
        "",
        _markdown_table(under_rejection, ["split_label", "dataset_id", "system_id", "corruption_family", "corruption_level", "seed_role", "corruption_seed", "accuracy", "f1", "unsafe_acceptance_rate", "rejection_rate"]),
        "",
        "## Unsafe Acceptance Survives",
        "",
        "Unsafe acceptance still survives in governance systems under severe specialist failure and confidence stress cases.",
        "",
        _markdown_table(surviving_unsafe, ["split_label", "dataset_id", "system_id", "corruption_family", "corruption_level", "seed_role", "corruption_seed", "unsafe_acceptance_rate", "rejection_rate"]),
        "",
        "## Most Damaging Corruption Families",
        "",
        _markdown_table(family_damage, ["corruption_family", "accuracy", "f1", "unsafe_acceptance_rate", "rejection_rate"]),
        "",
        "## Failure Mechanism Classification",
        "",
    ]
    for family, failure_class in sorted(FAILURE_CLASS.items()):
        lines.append(f"- `{family}`: `{failure_class}`.")
    lines.extend(
        [
            "",
            "## Linked Artifacts",
            "",
            "- Robustness tables: `results/reports/robustness_tables.csv`",
            "- System deltas: `results/reports/robustness_system_deltas.csv`",
            "- Locked metric rows: `results/metrics/locked_corruption/metric_rows.csv`",
            "- Audit metric rows: `results/metrics/audit_corruption/metric_rows.csv`",
            "- Unsafe acceptance figure: `results/figures/unsafe_acceptance_by_corruption.png`",
            "- Rejection figure: `results/figures/rejection_rate_by_corruption.png`",
            "",
        ]
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    # Phase 5 console.log: records Failure Map markdown persistence.
    console.log("phase5.failure_map.written", path=str(output_path), sha256=hash_file(output_path), damaging_family=str(family_damage.iloc[0]["corruption_family"]))
    return output_path


def _mean_delta(frame: pd.DataFrame, metric: str) -> float:
    subset = frame[frame["metric"] == metric]
    return float(subset["delta"].mean()) if not subset.empty else 0.0


def _markdown_table(frame: pd.DataFrame, columns: list[str]) -> str:
    if frame.empty:
        return "No rows matched this failure criterion."
    selected = frame[columns].copy()
    for column in selected.columns:
        if pd.api.types.is_float_dtype(selected[column]):
            selected[column] = selected[column].map(lambda value: f"{float(value):.6f}")
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = ["| " + " | ".join(str(value) for value in record) + " |" for record in selected.head(12).itertuples(index=False, name=None)]
    return "\n".join([header, separator, *rows])
