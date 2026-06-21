from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from mavs_ch10b.reporting.corruption_atlas import build_corruption_atlas
from mavs_ch10b.reporting.failure_map import build_failure_map
from mavs_ch10b.reporting.figures import build_report_figures
from mavs_ch10b.reporting.repro_manifest import build_reproducibility_manifest, validate_claim_support, write_reproducibility_manifest
from mavs_ch10b.reporting.tables import (
    SYSTEM_NAMES,
    build_robustness_table,
    build_summary_statistics,
    build_system_delta_table,
    load_area_rows,
    load_governance_distributions,
    load_metric_rows,
    write_csv,
)
from mavs_ch10b.verification.hash_utils import console, hash_file


def build_robustness_report(repo_root: Path, config_path: Path) -> dict[str, Any]:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    # Phase 5 console.log: records Robustness Report configuration loading.
    console.log("phase5.robustness_report.config_loaded", path=str(config_path), title=config["title"])
    metric_rows = load_metric_rows(repo_root)
    area_rows = load_area_rows(repo_root)
    severity_rows = load_governance_distributions(repo_root, "governance_severity_distribution.csv")
    threshold_rows = load_governance_distributions(repo_root, "governance_threshold_distribution.csv")
    system_deltas = build_system_delta_table(metric_rows)
    robustness_table = build_robustness_table(repo_root, metric_rows, area_rows)
    reports_dir = repo_root / "results" / "reports"
    write_csv(reports_dir / "robustness_tables.csv", robustness_table)
    write_csv(reports_dir / "robustness_system_deltas.csv", system_deltas)
    figures = build_report_figures(repo_root, metric_rows, area_rows, severity_rows, threshold_rows)
    atlas_path = build_corruption_atlas(repo_root, metric_rows, area_rows, reports_dir / "corruption_atlas.md")
    failure_map_path = build_failure_map(repo_root, metric_rows, system_deltas, reports_dir / "failure_map.md")
    summary = build_summary_statistics(metric_rows, area_rows, system_deltas, severity_rows, threshold_rows)
    report_path = reports_dir / "robustness_report.md"
    claim_support = build_claim_support(repo_root, summary, report_path, atlas_path, failure_map_path)
    validate_claim_support(repo_root, claim_support)
    render_robustness_report(repo_root, config, summary, figures, claim_support, report_path)
    validate_claim_support(repo_root, claim_support)
    output_paths = [
        report_path,
        atlas_path,
        failure_map_path,
        reports_dir / "robustness_tables.csv",
        reports_dir / "robustness_system_deltas.csv",
        *[Path(record["path"]) for record in figures],
    ]
    manifest = build_reproducibility_manifest(
        repo_root,
        config_path,
        output_paths,
        claim_support,
        row_counts={
            "metric_rows": int(metric_rows.shape[0]),
            "area_rows": int(area_rows.shape[0]),
            "robustness_table_rows": int(robustness_table.shape[0]),
            "system_delta_rows": int(system_deltas.shape[0]),
            "severity_rows": int(severity_rows.shape[0]),
            "threshold_rows": int(threshold_rows.shape[0]),
        },
        run_modes=summary["run_modes"],
    )
    manifest_path = reports_dir / "robustness_reproducibility_manifest.json"
    write_reproducibility_manifest(manifest_path, manifest)
    # Phase 5 console.log: records Robustness Report build completion.
    console.log("phase5.robustness_report.complete", report_path=str(report_path), manifest_path=str(manifest_path), claims=len(claim_support))
    return {"report_path": report_path, "manifest_path": manifest_path, "claim_support": claim_support}


def build_claim_support(repo_root: Path, summary: dict[str, Any], report_path: Path, atlas_path: Path, failure_map_path: Path) -> list[dict[str, Any]]:
    artifacts = {
        "tables": repo_root / "results" / "reports" / "robustness_tables.csv",
        "deltas": repo_root / "results" / "reports" / "robustness_system_deltas.csv",
        "atlas": atlas_path,
        "failure_map": failure_map_path,
        "area": repo_root / "results" / "robustness_curves" / "robustness_curve_area.csv",
        "locked_metrics": repo_root / "results" / "metrics" / "locked_corruption" / "metric_rows.csv",
        "audit_metrics": repo_root / "results" / "metrics" / "audit_corruption" / "metric_rows.csv",
        "severity_figure": repo_root / "results" / "figures" / "governance_severity_distribution.png",
        "unsafe_figure": repo_root / "results" / "figures" / "unsafe_acceptance_by_corruption.png",
    }
    pure_vs_veto = _delta(summary, "pure_mavs_gc", "veto_mavs")
    veto_vs_mean = _delta(summary, "veto_mavs", "mean_ensemble")
    most_damaging = summary["family_damage"][0]
    pure_overall = _system(summary["overall_system_means"], "pure_mavs_gc")
    claims = [
        _claim(
            "CLAIM-P5-001",
            "The Phase 5 report analyzes exploratory locked and audit stress runs, not final release-mode runs.",
            [artifacts["locked_metrics"], artifacts["audit_metrics"], artifacts["tables"]],
        ),
        _claim(
            "CLAIM-P5-002",
            f"Pure MAVS-GC suppresses unsafe acceptance relative to Veto MAVS on average, with mean unsafe delta {pure_vs_veto.get('unsafe_acceptance_rate', 0.0):.6f}.",
            [artifacts["deltas"], artifacts["tables"], artifacts["unsafe_figure"]],
        ),
        _claim(
            "CLAIM-P5-003",
            f"Pure MAVS-GC increases rejection relative to Veto MAVS on average, with mean rejection delta {pure_vs_veto.get('rejection_rate', 0.0):.6f}.",
            [artifacts["deltas"], artifacts["failure_map"]],
        ),
        _claim(
            "CLAIM-P5-004",
            f"Veto MAVS does not change the mean ensemble decision stream in the current artifacts; average accuracy delta is {veto_vs_mean.get('accuracy', 0.0):.6f}.",
            [artifacts["deltas"], artifacts["failure_map"]],
        ),
        _claim(
            "CLAIM-P5-005",
            f"The most damaging corruption family by mean accuracy is {most_damaging['corruption_family']} with mean accuracy {float(most_damaging['accuracy']):.6f}.",
            [artifacts["tables"], artifacts["atlas"], artifacts["failure_map"]],
        ),
        _claim(
            "CLAIM-P5-006",
            f"Pure MAVS-GC has the lowest overall unsafe acceptance mean among systems, {float(pure_overall['unsafe_acceptance_rate']):.6f}, but this is paired with high rejection.",
            [artifacts["tables"], artifacts["deltas"], artifacts["failure_map"]],
        ),
        _claim(
            "CLAIM-P5-007",
            "Technical failure rate is zero in the generated metric rows; observed failures are decision-quality and rejection-behavior failures.",
            [artifacts["tables"], artifacts["locked_metrics"], artifacts["audit_metrics"]],
        ),
        _claim(
            "CLAIM-P5-008",
            "Governance severity and threshold behavior are reported as trace-derived evidence, not as proof of safety by themselves.",
            [artifacts["severity_figure"], repo_root / "results" / "metrics" / "locked_corruption" / "governance_severity_distribution.csv", repo_root / "results" / "metrics" / "audit_corruption" / "governance_threshold_distribution.csv"],
        ),
    ]
    # Phase 5 console.log: records claim-support ledger construction.
    console.log("phase5.robustness_report.claim_support_built", claims=len(claims))
    return claims


def render_robustness_report(repo_root: Path, config: dict[str, Any], summary: dict[str, Any], figures: list[dict[str, Any]], claim_support: list[dict[str, Any]], output_path: Path) -> None:
    overall = {record["system_id"]: record for record in summary["overall_system_means"]}
    high = {record["system_id"]: record for record in summary["high_corruption_system_means"]}
    pure_vs_veto = _delta(summary, "pure_mavs_gc", "veto_mavs")
    veto_vs_mean = _delta(summary, "veto_mavs", "mean_ensemble")
    damaging_family = summary["family_damage"][0]
    figure_lines = [f"- `{_relative(repo_root, Path(record['path']))}` sha256 `{record['sha256']}`" for record in figures]
    claim_lines = [f"- `{claim['id']}`: {claim['text']} Support: {', '.join('`' + artifact['path'] + '`' for artifact in claim['artifacts'])}." for claim in claim_support]
    lines = [
        f"# {config['title']}",
        "",
        "## Source Documents and Mission",
        "",
        "This report is grounded in the Chapter 10B workplan source authority: `MAVS Chapter 10B.pdf`, `Mavs.pdf`, `Mavs Research Bible - Chapter 10.pdf`, and `MAVS Research Bible - Chapter 10A Completion Report.pdf`.",
        "",
        "Mission question: Does MAVS-GC fail more safely under adverse conditions?",
        "",
        "## Chapter 10A Dependency and Import Fidelity",
        "",
        "Chapter 10B imports the completed Chapter 10A foundation and performs no model training. The Phase 1 import report records Chapter 10A verification status `pass`; Phase 5 uses only generated Phase 3 and Phase 4 benchmark artifacts.",
        "",
        "## Methods",
        "",
        f"- Datasets: `{', '.join(summary['datasets'])}`.",
        f"- Systems: `{', '.join(summary['systems'])}`.",
        f"- Corruption families: `{', '.join(summary['corruption_families'])}`.",
        f"- Corruption levels: `{', '.join(str(value) for value in summary['levels'])}`.",
        f"- Metric rows analyzed: `{summary['metric_rows']}`.",
        f"- Robustness area rows analyzed: `{summary['area_rows']}`.",
        "",
        "## Benchmark Protocol",
        "",
        "Locked and audit benchmark splits are reported separately in `results/reports/robustness_tables.csv`. Locked uses the primary and shadow seed roles; audit uses audit and shadow seed roles. Shadow seeds are retained as verification stress evidence and are not used for tuning.",
        "",
        "## Anti-Overfitting Controls",
        "",
        f"- Run modes observed in Phase 4 metric rows: `{', '.join(summary['run_modes'])}`.",
        "- No Phase 5 code trains or tunes models, thresholds, weights, corruption levels, or seeds.",
        "- Conclusions are tied to claim IDs and artifact paths in `results/reports/robustness_reproducibility_manifest.json`.",
        "- The report does not claim universal robustness superiority because the evidence contains tradeoffs and negative cases.",
        "",
        "## Results",
        "",
        f"- Pure MAVS-GC overall mean accuracy: `{float(overall['pure_mavs_gc']['accuracy']):.6f}`.",
        f"- Pure MAVS-GC overall mean unsafe acceptance: `{float(overall['pure_mavs_gc']['unsafe_acceptance_rate']):.6f}`.",
        f"- Pure MAVS-GC overall mean rejection rate: `{float(overall['pure_mavs_gc']['rejection_rate']):.6f}`.",
        f"- Pure MAVS-GC vs Veto MAVS mean accuracy delta: `{pure_vs_veto.get('accuracy', 0.0):.6f}`.",
        f"- Pure MAVS-GC vs Veto MAVS mean unsafe acceptance delta: `{pure_vs_veto.get('unsafe_acceptance_rate', 0.0):.6f}`.",
        f"- Pure MAVS-GC vs Veto MAVS mean rejection delta: `{pure_vs_veto.get('rejection_rate', 0.0):.6f}`.",
        f"- Veto MAVS vs Mean Ensemble mean accuracy delta: `{veto_vs_mean.get('accuracy', 0.0):.6f}`.",
        f"- Most damaging corruption family by mean accuracy: `{damaging_family['corruption_family']}` with `{float(damaging_family['accuracy']):.6f}`.",
        f"- High-corruption Pure MAVS-GC mean unsafe acceptance: `{float(high['pure_mavs_gc']['unsafe_acceptance_rate']):.6f}`.",
        "",
        "## Final Answer to Chapter 10B",
        "",
        "The current exploratory evidence supports a qualified answer: Pure MAVS-GC often fails more safely by suppressing unsafe acceptance, especially against specialist failure, but it does so by increasing rejection and can produce severe over-rejection. Graceful degradation is not universal. Veto MAVS functions as a governance control in trace structure, but in these artifacts it does not materially change mean-ensemble decisions. MAVS failure modes are therefore not eliminated; they are shifted among unsafe acceptance, rejection, and accuracy/F1 loss.",
        "",
        "## Limitations",
        "",
        "- The full Phase 3 stress runs are marked `exploratory`; final release-mode verification is Phase 6 work.",
        "- Veto MAVS and Mean Ensemble are decision-identical in these artifacts, so Veto MAVS should not be treated as evidence of improved robustness here.",
        "- Pure MAVS-GC safety improvements are coupled to rejection behavior and cannot be reported as free predictive improvement.",
        "- Claims are limited to the four Chapter 10A datasets and the configured corruption grid.",
        "",
        "## Figures",
        "",
        *figure_lines,
        "",
        "## Claim Support Ledger",
        "",
        *claim_lines,
        "",
        "## Linked Final Artifacts",
        "",
        "- Robustness tables: `results/reports/robustness_tables.csv`",
        "- System deltas: `results/reports/robustness_system_deltas.csv`",
        "- Corruption Atlas: `results/reports/corruption_atlas.md`",
        "- Failure Map: `results/reports/failure_map.md`",
        "- Reproducibility manifest: `results/reports/robustness_reproducibility_manifest.json`",
        "",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    # Phase 5 console.log: records Robustness Report markdown persistence.
    console.log("phase5.robustness_report.written", path=str(output_path), sha256=hash_file(output_path), claims=len(claim_support))


def _claim(claim_id: str, text: str, artifacts: list[Path]) -> dict[str, Any]:
    return {
        "id": claim_id,
        "text": text,
        "artifacts": [{"path": str(path).replace("\\", "/") if not path.is_absolute() else _absolute_to_repo_path(path), "sha256": hash_file(path)} for path in artifacts],
    }


def _absolute_to_repo_path(path: Path) -> str:
    marker = "MAVS-Ch10B"
    parts = path.parts
    if marker in parts:
        index = parts.index(marker)
        return "/".join(parts[index + 1 :])
    return str(path).replace("\\", "/")


def _delta(summary: dict[str, Any], subject: str, baseline: str) -> dict[str, float]:
    output: dict[str, float] = {}
    for record in summary["delta_summary"]:
        if record["subject_system_id"] == subject and record["baseline_system_id"] == baseline:
            output[record["metric"]] = float(record["delta"])
    return output


def _system(records: list[dict[str, Any]], system_id: str) -> dict[str, Any]:
    for record in records:
        if record["system_id"] == system_id:
            return record
    raise KeyError(system_id)


def _relative(repo_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(repo_root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")
