from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from mavs_ch10b.reporting.tables import SYSTEM_NAMES
from mavs_ch10b.verification.hash_utils import console, hash_file


FAILURE_CLASS: dict[str, str] = {
    "feature_noise": "feature-driven",
    "missing_features": "feature-driven",
    "random_feature_deletion": "feature-driven",
    "label_noise": "label-driven",
    "confidence_distortion": "confidence-driven",
    "adversarial_confidence_inflation": "confidence-driven",
    "distribution_shift": "feature-driven distribution-shift",
    "synthetic_sensor_failure": "feature-driven sensor-failure",
    "specialist_failure": "specialist-driven",
}

EXPECTED_FAILURE_MODE: dict[str, str] = {
    "feature_noise": "Processed features move away from the Chapter 10A train distribution while preserving clean labels.",
    "missing_features": "Feature absence forces specialists and governance to operate with incomplete evidence.",
    "random_feature_deletion": "Random feature removal tests whether decisions depend on brittle individual coordinates.",
    "label_noise": "Observed-label corruption tests metric hygiene; clean labels remain the final authority.",
    "confidence_distortion": "Probability compression tests whether governance severity reacts to weaker confidence separation.",
    "adversarial_confidence_inflation": "Confidence inflation tests false certainty and unsafe acceptance pressure.",
    "distribution_shift": "Subset shift changes benchmark composition and tests out-of-distribution sensitivity.",
    "synthetic_sensor_failure": "Structured sensor-style failure tests correlated feature degradation.",
    "specialist_failure": "Specialist failure tests whether a damaged specialist can dominate or destabilize governance.",
}


def load_corruption_configs(repo_root: Path) -> dict[str, dict[str, Any]]:
    configs: dict[str, dict[str, Any]] = {}
    for path in sorted((repo_root / "configs" / "corruptions").glob("*.yaml")):
        if path.name == "corruption_grid.yaml":
            continue
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        configs[payload["corruption_family"]] = payload
        # Phase 5 console.log: records corruption config loading for the Corruption Atlas.
        console.log("phase5.corruption_atlas.config_loaded", path=str(path), corruption_family=payload["corruption_family"])
    return configs


def build_corruption_atlas(repo_root: Path, metric_rows: pd.DataFrame, area_rows: pd.DataFrame, output_path: Path | None = None) -> Path:
    output_path = output_path or repo_root / "results" / "reports" / "corruption_atlas.md"
    configs = load_corruption_configs(repo_root)
    lines = [
        "# Corruption Atlas",
        "",
        "This atlas covers every required Chapter 10B corruption family. Each section links implementation definition, parameterization, target space, expected failure mode, observed degradation, best and worst systems, and artifacts.",
        "",
        "Evidence source: `results/metrics/*_corruption/metric_rows.csv`, `results/robustness_curves/robustness_curve_area.csv`, and `results/corruption_manifests/corruption_grid_manifest.json`.",
        "",
    ]
    for family in sorted(configs):
        section = _family_section(repo_root, family, configs[family], metric_rows, area_rows)
        lines.extend(section)
        # Phase 5 console.log: records one Corruption Atlas family section construction.
        console.log("phase5.corruption_atlas.family_section_built", corruption_family=family)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    # Phase 5 console.log: records Corruption Atlas markdown persistence.
    console.log("phase5.corruption_atlas.written", path=str(output_path), sha256=hash_file(output_path), families=len(configs))
    return output_path


def _family_section(repo_root: Path, family: str, config: dict[str, Any], metric_rows: pd.DataFrame, area_rows: pd.DataFrame) -> list[str]:
    subset = metric_rows[metric_rows["corruption_family"] == family]
    area_subset = area_rows[area_rows["corruption_family"] == family]
    by_system = subset.groupby("system_id", as_index=False)[["accuracy", "f1", "unsafe_acceptance_rate", "rejection_rate"]].mean()
    best_accuracy = by_system.sort_values("accuracy", ascending=False).iloc[0]
    worst_accuracy = by_system.sort_values("accuracy", ascending=True).iloc[0]
    safest = by_system.sort_values("unsafe_acceptance_rate", ascending=True).iloc[0]
    highest_rejection = by_system.sort_values("rejection_rate", ascending=False).iloc[0]
    area_accuracy = area_subset[area_subset["metric"] == "accuracy"].groupby("system_id", as_index=False)["area"].mean().sort_values("area", ascending=False)
    best_area = area_accuracy.iloc[0] if not area_accuracy.empty else best_accuracy
    parameters = config.get("parameters", {})
    parameter_lines = [f"- `{key}`: `{value}`" for key, value in sorted(parameters.items())] or ["- No additional parameters."]
    target_spaces = ", ".join(sorted(str(value) for value in subset["corruption_target_space"].dropna().unique()))
    example_curve = repo_root / "results" / "robustness_curves" / f"{subset['dataset_id'].iloc[0]}__{subset['system_id'].iloc[0]}__{family}.csv"
    lines = [
        f"## {family}",
        "",
        "### Implementation Definition",
        "",
        config.get("description", "No description recorded."),
        "",
        "### Parameterization",
        "",
        *parameter_lines,
        "",
        "### Affected Target Space",
        "",
        f"- Config target space: `{config.get('target_space', 'unknown')}`",
        f"- Observed target space in metric rows: `{target_spaces}`",
        f"- Failure class: `{FAILURE_CLASS.get(family, 'unclassified')}`",
        "",
        "### Expected Failure Mode",
        "",
        EXPECTED_FAILURE_MODE.get(family, "Expected failure mode not classified."),
        "",
        "### Observed Degradation Pattern",
        "",
        f"- Mean accuracy across all systems: `{subset['accuracy'].mean():.6f}`.",
        f"- Mean unsafe acceptance across all systems: `{subset['unsafe_acceptance_rate'].mean():.6f}`.",
        f"- Mean rejection rate across all systems: `{subset['rejection_rate'].mean():.6f}`.",
        f"- Best average accuracy system: `{SYSTEM_NAMES.get(str(best_accuracy['system_id']), best_accuracy['system_id'])}` with `{float(best_accuracy['accuracy']):.6f}`.",
        f"- Lowest unsafe acceptance system: `{SYSTEM_NAMES.get(str(safest['system_id']), safest['system_id'])}` with `{float(safest['unsafe_acceptance_rate']):.6f}`.",
        f"- Highest rejection system: `{SYSTEM_NAMES.get(str(highest_rejection['system_id']), highest_rejection['system_id'])}` with `{float(highest_rejection['rejection_rate']):.6f}`.",
        "",
        "### Best and Worst Systems",
        "",
        f"- Best accuracy area system: `{SYSTEM_NAMES.get(str(best_area['system_id']), best_area['system_id'])}`.",
        f"- Worst average accuracy system: `{SYSTEM_NAMES.get(str(worst_accuracy['system_id']), worst_accuracy['system_id'])}` with `{float(worst_accuracy['accuracy']):.6f}`.",
        "",
        "### Linked Artifacts",
        "",
        "- Locked metric rows: `results/metrics/locked_corruption/metric_rows.csv`",
        "- Audit metric rows: `results/metrics/audit_corruption/metric_rows.csv`",
        "- Robustness area table: `results/robustness_curves/robustness_curve_area.csv`",
        f"- Example curve CSV: `{_relative(repo_root, example_curve)}`",
        "",
    ]
    return lines


def _relative(repo_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(repo_root)).replace("\\", "/")
    except ValueError:
        return str(path)
