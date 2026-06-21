from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

from mavs_ch10b.verification.artifact_inventory import CATEGORY_PATTERNS
from mavs_ch10b.verification.hash_utils import console, hash_file, hash_json, read_json
from mavs_ch10b.verification.import_audit import FORBIDDEN_TRAINING_TOKENS


REQUIRED_DATASETS = {"breast_cancer_wisconsin", "adult_income", "credit_card_fraud", "bank_marketing"}
REQUIRED_SYSTEMS = {"single_model", "mean_ensemble", "static_weighted_ensemble", "veto_mavs", "pure_mavs_gc"}
REQUIRED_FAMILIES = {
    "feature_noise",
    "missing_features",
    "random_feature_deletion",
    "label_noise",
    "confidence_distortion",
    "adversarial_confidence_inflation",
    "distribution_shift",
    "synthetic_sensor_failure",
    "specialist_failure",
}
REQUIRED_LEVELS = {"0.0", "0.05", "0.1", "0.2", "0.4", "0.6", "0.8", "1.0"}
EXPECTED_RUNS = {
    "locked": "phase3_locked_full_v1",
    "audit": "phase3_audit_full_v1",
}
EXPECTED_SYSTEM_RUNS = 7200
EXPECTED_TRACE_ARTIFACTS = 2880
EXPECTED_GRID_DEFINITIONS = 2880
REQUIRED_TRACE_FIELDS = {
    "run_id",
    "run_mode",
    "split_label",
    "dataset_id",
    "system_id",
    "corruption_family",
    "corruption_id",
    "corruption_level",
    "corruption_seed",
    "trace_path",
    "trace_sha256",
    "trace_rows",
    "trace_required",
    "trace_format",
    "trace_schema_hash",
}


@dataclass(frozen=True)
class GateCheck:
    name: str
    status: str
    summary: str
    evidence: dict[str, Any]


def verify_phase6_release(
    repo_root: Path,
    inventory_path: Path,
    report_path: Path,
    requested_run_mode: str,
) -> dict[str, Any]:
    resolved_root = repo_root.resolve()
    checks = [
        check_required_files(resolved_root, inventory_path, report_path),
        check_inventory_hashes(resolved_root, inventory_path),
        check_artifact_inventory_complete(inventory_path),
        check_ch10a_import_passed(resolved_root),
        check_no_retraining_artifacts(resolved_root),
        check_corruption_grid_complete(resolved_root),
        check_stress_matrix_complete(resolved_root),
        check_final_run_guards(resolved_root),
        check_metrics_cover_required_space(resolved_root),
        check_governance_trace_indexes(resolved_root),
        check_reports_reference_existing_artifacts(resolved_root),
        check_path_records_phase_evidence(resolved_root),
    ]
    overall_status = "pass" if all(check.status == "pass" for check in checks) else "fail"
    report = {
        "schema_version": "1.0",
        "phase": "phase6",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "requested_run_mode": requested_run_mode,
        "verification_scope": "prepared-checkout artifact integrity and release guard validation",
        "overall_status": overall_status,
        "checks": [asdict(check) for check in checks],
    }
    write_verification_report(report_path, report)
    # Phase 6 console.log: records final verification gate completion.
    console.log(
        "phase6.verify.complete",
        report_path=str(report_path),
        overall_status=overall_status,
        checks=len(checks),
        failures=[check.name for check in checks if check.status != "pass"],
    )
    return report


def check_required_files(repo_root: Path, inventory_path: Path, report_path: Path) -> GateCheck:
    required = [
        repo_root / "scripts" / "reproduce_all.py",
        repo_root / "scripts" / "hash_artifacts.py",
        repo_root / "scripts" / "verify_artifacts.py",
        repo_root / "tests" / "test_end_to_end_smoke.py",
        repo_root / "tests" / "test_artifact_inventory_complete.py",
        repo_root / "tests" / "test_final_run_guards.py",
        inventory_path,
        repo_root / "WorkPlan.md",
        repo_root / "Path.md",
    ]
    missing = [_relative(repo_root, path) for path in required if not path.exists()]
    if report_path.exists():
        report_state = "existing"
    else:
        report_state = "will_be_written_by_verify_artifacts"
    # Phase 6 console.log: records required-file gate evaluation.
    console.log("phase6.verify.required_files_checked", missing=missing, verification_report_state=report_state)
    return _check(
        "required_files_exist",
        not missing,
        f"{len(required) - len(missing)} required files are present; verification report state is {report_state}.",
        {"missing": missing, "verification_report_path": _relative(repo_root, report_path), "verification_report_state": report_state},
    )


def check_inventory_hashes(repo_root: Path, inventory_path: Path) -> GateCheck:
    inventory = read_json(inventory_path)
    mismatches: list[dict[str, str]] = []
    missing: list[str] = []
    for artifact in inventory.get("artifacts", []):
        path = repo_root / str(artifact["path"])
        if not path.exists():
            missing.append(str(artifact["path"]))
            continue
        actual = hash_file(path)
        if actual != str(artifact["sha256"]):
            mismatches.append({"path": str(artifact["path"]), "expected": str(artifact["sha256"]), "actual": actual})
    passed = not missing and not mismatches
    # Phase 6 console.log: records artifact-inventory hash gate evaluation.
    console.log("phase6.verify.inventory_hashes_checked", artifacts=len(inventory.get("artifacts", [])), missing=len(missing), mismatches=len(mismatches))
    return _check(
        "hashes_match",
        passed,
        f"{len(inventory.get('artifacts', []))} inventory artifacts were hash-checked.",
        {"missing": missing[:20], "mismatches": mismatches[:20]},
    )


def check_artifact_inventory_complete(inventory_path: Path) -> GateCheck:
    inventory = read_json(inventory_path)
    counts = {category: int(inventory.get("category_counts", {}).get(category, 0)) for category in CATEGORY_PATTERNS}
    missing_categories = [category for category, count in counts.items() if count <= 0]
    # Phase 6 console.log: records artifact-inventory completeness gate evaluation.
    console.log("phase6.verify.inventory_completeness_checked", category_counts=counts, missing_categories=missing_categories)
    return _check(
        "artifact_inventory_complete",
        not missing_categories,
        "All WorkPlan-required artifact categories are represented.",
        {"category_counts": counts, "missing_categories": missing_categories},
    )


def check_ch10a_import_passed(repo_root: Path) -> GateCheck:
    import_path = repo_root / "results" / "baseline_import" / "ch10a_import_manifest.json"
    manifest = read_json(import_path)
    imported_datasets = set(manifest.get("imported_dataset_ids", []))
    imported_systems = set(manifest.get("imported_system_ids", []))
    validation = manifest.get("validation", {})
    passed = (
        manifest.get("verification_report_status") == "pass"
        and imported_datasets == REQUIRED_DATASETS
        and imported_systems == REQUIRED_SYSTEMS
        and not validation.get("missing_required_files")
        and not validation.get("inventory_mismatches")
        and not validation.get("trace_schema_failures")
    )
    # Phase 6 console.log: records Chapter 10A import gate evaluation.
    console.log(
        "phase6.verify.ch10a_import_checked",
        status=manifest.get("verification_report_status"),
        datasets=sorted(imported_datasets),
        systems=sorted(imported_systems),
    )
    return _check(
        "chapter10a_import_passed",
        passed,
        "Chapter 10A imported foundation remains validated by the Phase 1 manifest.",
        {
            "manifest_path": _relative(repo_root, import_path),
            "manifest_sha256": hash_file(import_path),
            "verification_report_status": manifest.get("verification_report_status"),
            "source_git_commit": manifest.get("source_git_commit"),
            "trace_records_checked": validation.get("trace_records_checked"),
        },
    )


def check_no_retraining_artifacts(repo_root: Path) -> GateCheck:
    model_suffixes = {".joblib", ".pkl", ".pickle", ".sav", ".pt", ".pth", ".onnx"}
    generated_models = [
        _relative(repo_root, path)
        for path in (repo_root / "results").rglob("*")
        if path.is_file() and path.suffix.lower() in model_suffixes
    ]
    forbidden_commands = _forbidden_commands_in_manifests(repo_root)
    passed = not generated_models and not forbidden_commands
    # Phase 6 console.log: records no-retraining artifact gate evaluation.
    console.log(
        "phase6.verify.no_retraining_checked",
        generated_models=len(generated_models),
        forbidden_commands=len(forbidden_commands),
        forbidden_tokens=list(FORBIDDEN_TRAINING_TOKENS),
    )
    return _check(
        "no_retraining_performed",
        passed,
        "No Chapter 10B result directory model-training artifacts or forbidden training commands were detected.",
        {"generated_model_artifacts": generated_models, "forbidden_manifest_commands": forbidden_commands},
    )


def check_corruption_grid_complete(repo_root: Path) -> GateCheck:
    grid_path = repo_root / "results" / "corruption_manifests" / "corruption_grid_manifest.json"
    manifest = read_json(grid_path)
    primary = set(manifest.get("primary_seeds", []))
    audit = set(manifest.get("audit_seeds", []))
    passed = (
        int(manifest.get("definition_count", -1)) == EXPECTED_GRID_DEFINITIONS
        and set(manifest.get("datasets", [])) == REQUIRED_DATASETS
        and set(manifest.get("corruption_families", [])) == REQUIRED_FAMILIES
        and {str(level) for level in manifest.get("levels", [])} == REQUIRED_LEVELS
        and primary.isdisjoint(audit)
    )
    # Phase 6 console.log: records corruption-grid gate evaluation.
    console.log(
        "phase6.verify.corruption_grid_checked",
        definitions=manifest.get("definition_count"),
        primary_seeds=sorted(primary),
        audit_seeds=sorted(audit),
        seed_overlap=sorted(primary.intersection(audit)),
    )
    return _check(
        "corruption_grid_complete",
        passed,
        "The corruption grid has the required datasets, corruptions, levels, and independent locked/audit seeds.",
        {
            "definition_count": manifest.get("definition_count"),
            "datasets": manifest.get("datasets", []),
            "corruption_families": manifest.get("corruption_families", []),
            "levels": manifest.get("levels", []),
            "seed_overlap": sorted(primary.intersection(audit)),
            "grid_manifest_sha256": hash_file(grid_path),
        },
    )


def check_stress_matrix_complete(repo_root: Path) -> GateCheck:
    manifests = _load_run_manifests(repo_root)
    failures: list[str] = []
    evidence: dict[str, Any] = {}
    for split_label, manifest in manifests.items():
        run_id = EXPECTED_RUNS[split_label]
        config_hash_actual = _config_hash(repo_root, manifest)
        checks = {
            "run_status": manifest.get("run_status") == "complete",
            "system_run_count": int(manifest.get("system_run_count", -1)) == EXPECTED_SYSTEM_RUNS,
            "trace_artifact_count": int(manifest.get("governance_trace_artifact_count", -1)) == EXPECTED_TRACE_ARTIFACTS,
            "aggregate_row_count": int(manifest.get("aggregate_row_count", -1)) == EXPECTED_TRACE_ARTIFACTS,
            "config_hash_matches": config_hash_actual == manifest.get("config_hash"),
            "import_hash_matches": _current_hash_matches(manifest, "chapter10a_import_manifest_path", "chapter10a_import_manifest_sha256"),
            "grid_hash_matches": _current_hash_matches(manifest, "corruption_grid_manifest_path", "corruption_grid_manifest_sha256"),
            "prediction_index_hash_matches": _current_hash_matches(manifest, "prediction_index_path", "prediction_index_sha256"),
            "trace_index_hash_matches": _current_hash_matches(manifest, "trace_index_path", "trace_index_sha256"),
            "aggregate_index_hash_matches": _current_hash_matches(manifest, "aggregate_index_path", "aggregate_index_sha256"),
        }
        if not all(checks.values()):
            failures.extend(f"{run_id}:{name}" for name, ok in checks.items() if not ok)
        evidence[split_label] = {
            "run_id": run_id,
            "run_mode": manifest.get("run_mode"),
            "system_run_count": manifest.get("system_run_count"),
            "governance_trace_artifact_count": manifest.get("governance_trace_artifact_count"),
            "config_hash_expected": manifest.get("config_hash"),
            "config_hash_actual": config_hash_actual,
            "checks": checks,
        }
    # Phase 6 console.log: records stress-matrix gate evaluation.
    console.log("phase6.verify.stress_matrix_checked", failures=failures, runs=list(evidence))
    return _check(
        "stress_matrix_complete",
        not failures,
        "Locked and audit stress matrices are complete and their referenced hashes still match.",
        {"runs": evidence, "failures": failures},
    )


def check_final_run_guards(repo_root: Path) -> GateCheck:
    manifests = list(_load_run_manifests(repo_root).values())
    exploratory_final_violations = final_run_mode_violations(manifests)
    seed_overlap = audit_seed_overlap(repo_root)
    import_hash_changes = _import_hash_changes_after_phase1(repo_root, manifests)
    config_changes = _final_config_hash_changes(repo_root, manifests)
    training_artifacts = check_no_retraining_artifacts(repo_root).evidence["generated_model_artifacts"]
    passed = not exploratory_final_violations and not seed_overlap and not import_hash_changes and not config_changes and not training_artifacts
    # Phase 6 console.log: records anti-overfitting final-run guard evaluation.
    console.log(
        "phase6.verify.final_guards_checked",
        exploratory_final_violations=exploratory_final_violations,
        seed_overlap=seed_overlap,
        import_hash_changes=import_hash_changes,
        config_changes=config_changes,
        training_artifacts=training_artifacts,
    )
    return _check(
        "anti_overfitting_final_run_guards",
        passed,
        "Final-run guards are armed; archived exploratory runs are not certified as final runs.",
        {
            "exploratory_final_violations": exploratory_final_violations,
            "seed_overlap": seed_overlap,
            "import_hash_changes": import_hash_changes,
            "final_config_hash_changes": config_changes,
            "training_artifacts": training_artifacts,
            "current_run_modes": sorted({str(manifest.get("run_mode")) for manifest in manifests}),
        },
    )


def check_metrics_cover_required_space(repo_root: Path) -> GateCheck:
    failures: list[str] = []
    evidence: dict[str, Any] = {}
    for split_label in ("locked", "audit"):
        metric_path = repo_root / "results" / "metrics" / f"{split_label}_corruption" / "metric_rows.csv"
        rows = _read_csv(metric_path)
        datasets = {row["dataset_id"] for row in rows}
        systems = {row["system_id"] for row in rows}
        families = {row["corruption_family"] for row in rows}
        levels = {row["corruption_level"] for row in rows}
        if len(rows) != EXPECTED_SYSTEM_RUNS:
            failures.append(f"{split_label}:metric_rows")
        if datasets != REQUIRED_DATASETS:
            failures.append(f"{split_label}:datasets")
        if systems != REQUIRED_SYSTEMS:
            failures.append(f"{split_label}:systems")
        if families != REQUIRED_FAMILIES:
            failures.append(f"{split_label}:families")
        if levels != REQUIRED_LEVELS:
            failures.append(f"{split_label}:levels")
        evidence[split_label] = {
            "rows": len(rows),
            "datasets": sorted(datasets),
            "systems": sorted(systems),
            "families": sorted(families),
            "levels": sorted(levels),
            "metric_rows_sha256": hash_file(metric_path),
        }
    # Phase 6 console.log: records metric coverage gate evaluation.
    console.log("phase6.verify.metrics_coverage_checked", failures=failures)
    return _check(
        "metrics_cover_required_space",
        not failures,
        "Metric rows cover all required datasets, systems, corruption families, and levels for locked and audit splits.",
        {"splits": evidence, "failures": failures},
    )


def check_governance_trace_indexes(repo_root: Path) -> GateCheck:
    failures: list[str] = []
    evidence: dict[str, Any] = {}
    for split_label, run_id in EXPECTED_RUNS.items():
        trace_path = repo_root / "results" / "stress_runs" / f"{run_id}_trace_index.csv"
        rows = _read_csv(trace_path)
        header = set(rows[0]) if rows else set()
        missing_fields = sorted(REQUIRED_TRACE_FIELDS - header)
        invalid_rows = [
            index
            for index, row in enumerate(rows[:50], start=1)
            if row.get("trace_required") != "True"
            or row.get("trace_format") != "columnar_npz"
            or not row.get("trace_schema_hash")
            or not row.get("trace_sha256")
            or int(row.get("trace_rows", "0")) <= 0
        ]
        if len(rows) != EXPECTED_TRACE_ARTIFACTS:
            failures.append(f"{run_id}:trace_count")
        if missing_fields:
            failures.append(f"{run_id}:missing_fields")
        if invalid_rows:
            failures.append(f"{run_id}:invalid_trace_rows")
        evidence[split_label] = {
            "run_id": run_id,
            "trace_rows": len(rows),
            "missing_fields": missing_fields,
            "sample_invalid_rows": invalid_rows[:10],
            "trace_index_sha256": hash_file(trace_path),
        }
    # Phase 6 console.log: records governance trace-index gate evaluation.
    console.log("phase6.verify.trace_indexes_checked", failures=failures)
    return _check(
        "governance_traces_contain_required_fields",
        not failures,
        "Trace indexes contain the required governance fields, schema hashes, and row counts.",
        {"splits": evidence, "failures": failures},
    )


def check_reports_reference_existing_artifacts(repo_root: Path) -> GateCheck:
    manifest_path = repo_root / "results" / "reports" / "robustness_reproducibility_manifest.json"
    manifest = read_json(manifest_path)
    failures: list[str] = []
    checked = 0
    report_text = (repo_root / "results" / "reports" / "robustness_report.md").read_text(encoding="utf-8")
    for artifact in manifest.get("inputs", []) + manifest.get("outputs", []):
        checked += 1
        _validate_report_artifact(repo_root, artifact, failures)
    for claim in manifest.get("claim_support", []):
        if str(claim.get("id")) not in report_text:
            failures.append(f"claim_missing_from_report:{claim.get('id')}")
        for artifact in claim.get("artifacts", []):
            checked += 1
            _validate_report_artifact(repo_root, artifact, failures)
    # Phase 6 console.log: records report reference gate evaluation.
    console.log("phase6.verify.report_references_checked", checked=checked, failures=failures[:20])
    return _check(
        "reports_reference_existing_artifacts",
        not failures,
        "Report claims and manifest input/output records reference existing artifacts with matching hashes.",
        {"checked_artifacts": checked, "failures": failures[:20]},
    )


def check_path_records_phase_evidence(repo_root: Path) -> GateCheck:
    path_text = (repo_root / "Path.md").read_text(encoding="utf-8")
    required_markers = [f"Phase {index}" for index in range(1, 7)]
    missing = [marker for marker in required_markers if marker not in path_text]
    console_mentions = path_text.count("console.log")
    passed = not missing and console_mentions >= 6
    # Phase 6 console.log: records Path.md evidence gate evaluation.
    console.log("phase6.verify.path_evidence_checked", missing=missing, console_mentions=console_mentions)
    return _check(
        "path_records_all_phase_evidence",
        passed,
        "Path.md records the phase trail and console log inventory.",
        {"missing_phase_markers": missing, "console_log_mentions": console_mentions},
    )


def final_run_mode_violations(run_manifests: Iterable[dict[str, Any]]) -> list[str]:
    violations: list[str] = []
    for manifest in run_manifests:
        run_id = str(manifest.get("run_id", ""))
        run_mode = str(manifest.get("run_mode", ""))
        if _is_final_run_manifest(manifest) and run_mode != "final":
            violations.append(f"{run_id}:{run_mode}")
    return violations


def audit_seed_overlap(repo_root: Path) -> list[int]:
    manifest = read_json(repo_root / "results" / "corruption_manifests" / "corruption_grid_manifest.json")
    return sorted(set(manifest.get("primary_seeds", [])).intersection(set(manifest.get("audit_seeds", []))))


def write_verification_report(report_path: Path, report: dict[str, Any]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# MAVS Chapter 10B Phase 6 Verification Report",
        "",
        f"Generated at UTC: `{report['generated_at_utc']}`",
        f"Requested run mode: `{report['requested_run_mode']}`",
        f"Verification scope: `{report['verification_scope']}`",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Gate Results",
        "",
        "| Check | Status | Summary |",
        "| --- | --- | --- |",
    ]
    for check in report["checks"]:
        lines.append(f"| `{check['name']}` | `{check['status']}` | {check['summary']} |")
    lines.extend(["", "## Evidence", ""])
    for check in report["checks"]:
        lines.extend(
            [
                f"### {check['name']}",
                "",
                f"Status: `{check['status']}`",
                "",
                "```json",
                json.dumps(check["evidence"], indent=2, sort_keys=True, default=str),
                "```",
                "",
            ]
        )
    report_path.write_text("\n".join(lines), encoding="utf-8")
    # Phase 6 console.log: records verification report persistence.
    console.log("phase6.verify.report_written", path=str(report_path), sha256=hash_file(report_path), overall_status=report["overall_status"])


def _check(name: str, passed: bool, summary: str, evidence: dict[str, Any]) -> GateCheck:
    return GateCheck(name=name, status="pass" if passed else "fail", summary=summary, evidence=evidence)


def _load_run_manifests(repo_root: Path) -> dict[str, dict[str, Any]]:
    return {
        split_label: read_json(repo_root / "results" / "stress_runs" / f"{run_id}_run_manifest.json")
        for split_label, run_id in EXPECTED_RUNS.items()
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _config_hash(repo_root: Path, manifest: dict[str, Any]) -> str:
    config_path = _resolve_path(repo_root, str(manifest["config_path"]))
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return hash_json(config)


def _current_hash_matches(manifest: dict[str, Any], path_key: str, hash_key: str) -> bool:
    path = Path(str(manifest[path_key]))
    return path.exists() and hash_file(path) == str(manifest[hash_key])


def _forbidden_commands_in_manifests(repo_root: Path) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for manifest_path in repo_root.glob("results/**/*.json"):
        if manifest_path.name == "artifact_inventory.json":
            continue
        try:
            manifest = read_json(manifest_path)
        except json.JSONDecodeError:
            continue
        command_line = " ".join(str(item).lower() for item in manifest.get("command_line", []))
        forbidden = [token for token in FORBIDDEN_TRAINING_TOKENS if token.lower() in command_line]
        if forbidden:
            failures.append({"path": _relative(repo_root, manifest_path), "forbidden": forbidden, "command_line": manifest.get("command_line", [])})
    return failures


def _import_hash_changes_after_phase1(repo_root: Path, manifests: list[dict[str, Any]]) -> list[str]:
    import_path = repo_root / "results" / "baseline_import" / "ch10a_import_manifest.json"
    actual = hash_file(import_path)
    expected_hashes = {str(manifest.get("chapter10a_import_manifest_sha256", "")) for manifest in manifests}
    config_expected = _experiment_expected_import_hashes(repo_root)
    expected_hashes.update(config_expected)
    return sorted(expected for expected in expected_hashes if expected and expected != actual)


def _experiment_expected_import_hashes(repo_root: Path) -> set[str]:
    hashes: set[str] = set()
    for path in repo_root.glob("configs/experiments/*corruption_benchmark.yaml"):
        config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        value = str(config.get("expected_ch10a_import_manifest_sha256", ""))
        if value:
            hashes.add(value)
    return hashes


def _final_config_hash_changes(repo_root: Path, manifests: list[dict[str, Any]]) -> list[str]:
    failures: list[str] = []
    for manifest in manifests:
        if not _is_final_run_manifest(manifest):
            continue
        actual = _config_hash(repo_root, manifest)
        if actual != str(manifest.get("config_hash", "")):
            failures.append(str(manifest.get("run_id", "")))
    return failures


def _is_final_run_manifest(manifest: dict[str, Any]) -> bool:
    run_id = str(manifest.get("run_id", "")).lower()
    run_mode = str(manifest.get("run_mode", "")).lower()
    return run_mode == "final" or "final" in run_id


def _validate_report_artifact(repo_root: Path, artifact: dict[str, Any], failures: list[str]) -> None:
    relative = str(artifact.get("path", ""))
    path = repo_root / relative
    if not path.exists():
        failures.append(f"missing:{relative}")
        return
    expected = str(artifact.get("sha256", ""))
    actual = hash_file(path)
    if expected != actual:
        failures.append(f"hash_mismatch:{relative}")


def _resolve_path(repo_root: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        if candidate.exists():
            return candidate
        parts = list(candidate.parts)
        if repo_root.name in parts:
            return repo_root / Path(*parts[parts.index(repo_root.name) + 1 :])
        return candidate
    return repo_root / candidate


def _relative(repo_root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root)).replace("\\", "/")
    except ValueError:
        return str(path)
