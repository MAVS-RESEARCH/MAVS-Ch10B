from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mavs_ch10b.verification.hash_utils import console, hash_file


def build_report_figures(repo_root: Path, metric_rows: pd.DataFrame, area_rows: pd.DataFrame, severity_rows: pd.DataFrame, threshold_rows: pd.DataFrame) -> list[dict[str, Any]]:
    output_dir = repo_root / "results" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    figures = [
        _plot_governance_distribution(output_dir / "governance_severity_distribution.png", severity_rows, "severity_mean", "Governance Severity Mean by Corruption Family"),
        _plot_governance_distribution(output_dir / "threshold_distribution.png", threshold_rows, "theta_mean", "Governance Threshold Mean by Corruption Family"),
        _plot_metric_by_family(output_dir / "unsafe_acceptance_by_corruption.png", metric_rows, "unsafe_acceptance_rate", "Unsafe Acceptance Rate by Corruption Family"),
        _plot_area_by_system(output_dir / "robustness_area_by_system.png", area_rows),
        _plot_rejection_by_level(output_dir / "rejection_rate_by_corruption.png", metric_rows),
        _plot_failure_heatmap(output_dir / "failure_rate_heatmap.png", metric_rows),
    ]
    # Phase 5 console.log: records completion of all report figure generation.
    console.log("phase5.figures.figure_set_built", figures=len(figures))
    return figures


def _plot_governance_distribution(path: Path, frame: pd.DataFrame, metric: str, title: str) -> dict[str, Any]:
    # Phase 5 console.log: records governance distribution figure build dispatch.
    console.log("phase5.figures.governance_distribution_start", path=str(path), metric=metric)
    grouped = frame.groupby(["corruption_family", "system_id"], as_index=False)[metric].mean()
    pivot = grouped.pivot(index="corruption_family", columns="system_id", values=metric).fillna(0.0)
    ax = pivot.plot(kind="bar", figsize=(14, 6), width=0.82)
    ax.set_title(title)
    ax.set_xlabel("Corruption family")
    ax.set_ylabel(metric)
    ax.tick_params(axis="x", labelrotation=45)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(title="System")
    plt.tight_layout()
    return _save(path)


def _plot_metric_by_family(path: Path, frame: pd.DataFrame, metric: str, title: str) -> dict[str, Any]:
    # Phase 5 console.log: records metric-by-family figure build dispatch.
    console.log("phase5.figures.metric_by_family_start", path=str(path), metric=metric)
    grouped = frame.groupby(["corruption_family", "system_id"], as_index=False)[metric].mean()
    pivot = grouped.pivot(index="corruption_family", columns="system_id", values=metric).fillna(0.0)
    ax = pivot.plot(kind="bar", figsize=(14, 6), width=0.82)
    ax.set_title(title)
    ax.set_xlabel("Corruption family")
    ax.set_ylabel(metric)
    ax.tick_params(axis="x", labelrotation=45)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(title="System")
    plt.tight_layout()
    return _save(path)


def _plot_area_by_system(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    # Phase 5 console.log: records robustness-area figure build dispatch.
    console.log("phase5.figures.area_by_system_start", path=str(path))
    selected = frame[frame["metric"].isin(["accuracy", "f1", "unsafe_acceptance_rate", "technical_failure_rate", "rejection_rate"])]
    grouped = selected.groupby(["system_id", "metric"], as_index=False)["area"].mean()
    pivot = grouped.pivot(index="system_id", columns="metric", values="area").fillna(0.0)
    ax = pivot.plot(kind="bar", figsize=(12, 6), width=0.82)
    ax.set_title("Average Robustness Curve Area by System")
    ax.set_xlabel("System")
    ax.set_ylabel("Trapezoidal area")
    ax.tick_params(axis="x", labelrotation=30)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(title="Metric")
    plt.tight_layout()
    return _save(path)


def _plot_rejection_by_level(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    # Phase 5 console.log: records rejection-rate figure build dispatch.
    console.log("phase5.figures.rejection_by_level_start", path=str(path))
    grouped = frame.groupby(["corruption_level", "system_id"], as_index=False)["rejection_rate"].mean()
    pivot = grouped.pivot(index="corruption_level", columns="system_id", values="rejection_rate").sort_index().fillna(0.0)
    ax = pivot.plot(kind="line", marker="o", figsize=(12, 6))
    ax.set_title("Rejection Rate by Corruption Level")
    ax.set_xlabel("Corruption level")
    ax.set_ylabel("Rejection rate")
    ax.grid(alpha=0.25)
    ax.legend(title="System")
    plt.tight_layout()
    return _save(path)


def _plot_failure_heatmap(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    # Phase 5 console.log: records technical-failure heatmap build dispatch.
    console.log("phase5.figures.failure_heatmap_start", path=str(path))
    grouped = frame.groupby(["corruption_family", "system_id"], as_index=False)["technical_failure_rate"].mean()
    pivot = grouped.pivot(index="corruption_family", columns="system_id", values="technical_failure_rate").fillna(0.0)
    fig, ax = plt.subplots(figsize=(10, 7))
    image = ax.imshow(pivot.to_numpy(dtype=float), aspect="auto", cmap="viridis", vmin=0.0, vmax=max(1.0, float(pivot.to_numpy(dtype=float).max(initial=0.0))))
    ax.set_title("Technical Failure Rate Heatmap")
    ax.set_xticks(np.arange(len(pivot.columns)))
    ax.set_yticks(np.arange(len(pivot.index)))
    ax.set_xticklabels(pivot.columns, rotation=30, ha="right")
    ax.set_yticklabels(pivot.index)
    for row_index, family in enumerate(pivot.index):
        for column_index, system in enumerate(pivot.columns):
            ax.text(column_index, row_index, f"{pivot.loc[family, system]:.3f}", ha="center", va="center", color="white" if pivot.loc[family, system] > 0.5 else "black", fontsize=8)
    fig.colorbar(image, ax=ax, label="technical_failure_rate")
    plt.tight_layout()
    return _save(path)


def _save(path: Path) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=160)
    plt.close()
    record = {"path": str(path), "sha256": hash_file(path)}
    # Phase 5 console.log: records report figure artifact persistence.
    console.log("phase5.figures.figure_written", path=str(path), sha256=record["sha256"])
    return record
