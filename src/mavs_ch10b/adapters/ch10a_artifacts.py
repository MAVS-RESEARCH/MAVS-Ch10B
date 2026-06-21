from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mavs_ch10b.adapters.ch10a_source import Chapter10ASource
from mavs_ch10b.verification.hash_utils import console, git_commit, hash_file, read_json


REQUIRED_DATASET_IDS: tuple[str, ...] = (
    "breast_cancer_wisconsin",
    "adult_income",
    "credit_card_fraud",
    "bank_marketing",
)
REQUIRED_SPECIALIST_IDS: tuple[str, ...] = ("random_forest", "gradient_boosted_trees", "mlp")
REQUIRED_SYSTEM_IDS: tuple[str, ...] = (
    "single_model",
    "mean_ensemble",
    "static_weighted_ensemble",
    "veto_mavs",
    "pure_mavs_gc",
)
BENCHMARK_SPLITS: dict[str, str] = {"locked": "locked_benchmark", "audit": "audit_benchmark"}
REQUIRED_SYSTEM_CONFIGS: tuple[str, ...] = (
    "single_model",
    "mean_ensemble",
    "static_weighted_ensemble",
    "veto_mavs",
    "pure_mavs_gc",
    "governance_defaults",
)
CH10A_TRACE_FIELDS: tuple[str, ...] = (
    "x_id",
    "dataset_id",
    "split",
    "system_id",
    "specialist_ids",
    "s",
    "r",
    "z",
    "a",
    "w",
    "m",
    "theta",
    "R",
    "hard_veto",
    "decision",
    "label",
    "config_hash",
    "checkpoint_hashes",
    "trace_hash",
)


@dataclass(frozen=True)
class FoundationValidation:
    verification_report_status: str
    required_files_checked: int
    missing_required_files: tuple[str, ...]
    inventory_checked_artifacts: int
    inventory_missing: tuple[str, ...]
    inventory_mismatches: tuple[str, ...]
    trace_records_checked: int
    trace_schema_failures: tuple[str, ...]
    config_hashes: dict[str, str]
    checkpoint_hashes: dict[str, dict[str, str]]
    split_hashes: dict[str, dict[str, str]]
    current_source_git_commit: str
    manifest_git_commit: str

    @property
    def passed(self) -> bool:
        return (
            self.verification_report_status == "pass"
            and not self.missing_required_files
            and not self.inventory_missing
            and not self.inventory_mismatches
            and not self.trace_schema_failures
        )


def validate_ch10a_foundation(
    source: Chapter10ASource,
    *,
    verify_inventory: bool = True,
    verify_trace_schema: bool = True,
) -> FoundationValidation:
    repo_root = source.repo_root
    required_files = required_foundation_paths(repo_root)
    missing = tuple(str(path) for path in required_files if not path.exists())
    # Phase 1 console.log: records required Chapter 10A file presence validation.
    console.log("phase1.ch10a_artifacts.required_files_checked", checked=len(required_files), missing=len(missing))

    verification_status = verification_report_status(repo_root / str(source.config["verification_report_path"]))
    # Phase 1 console.log: records Chapter 10A verification report status extraction.
    console.log("phase1.ch10a_artifacts.verification_report_status", status=verification_status)

    inventory_missing: tuple[str, ...] = ()
    inventory_mismatches: tuple[str, ...] = ()
    inventory_checked = 0
    if verify_inventory:
        inventory = read_json(repo_root / str(source.config["artifact_inventory_path"]))
        inventory_result = verify_inventory_hashes(repo_root, inventory)
        inventory_checked = int(inventory_result["checked"])
        inventory_missing = tuple(inventory_result["missing"])
        inventory_mismatches = tuple(inventory_result["mismatches"])
        # Phase 1 console.log: records Chapter 10A artifact inventory hash validation.
        console.log(
            "phase1.ch10a_artifacts.inventory_hashes_checked",
            checked=inventory_checked,
            missing=len(inventory_missing),
            mismatches=len(inventory_mismatches),
        )

    trace_checked = 0
    trace_failures: tuple[str, ...] = ()
    if verify_trace_schema:
        trace_result = validate_governance_trace_schema(repo_root)
        trace_checked = int(trace_result["checked_records"])
        trace_failures = tuple(trace_result["failures"])
        # Phase 1 console.log: records Chapter 10A governance trace schema validation.
        console.log("phase1.ch10a_artifacts.trace_schema_checked", checked_records=trace_checked, failures=len(trace_failures))

    reproducibility_manifest = read_json(repo_root / str(source.config["reproducibility_manifest_path"]))
    validation = FoundationValidation(
        verification_report_status=verification_status,
        required_files_checked=len(required_files),
        missing_required_files=missing,
        inventory_checked_artifacts=inventory_checked,
        inventory_missing=inventory_missing,
        inventory_mismatches=inventory_mismatches,
        trace_records_checked=trace_checked,
        trace_schema_failures=trace_failures,
        config_hashes=collect_config_hashes(repo_root),
        checkpoint_hashes=collect_checkpoint_hashes(repo_root),
        split_hashes=collect_split_hashes(repo_root),
        current_source_git_commit=git_commit(repo_root),
        manifest_git_commit=str(reproducibility_manifest.get("git_commit", "unavailable")),
    )
    # Phase 1 console.log: records complete Chapter 10A foundation validation result.
    console.log(
        "phase1.ch10a_artifacts.validation_complete",
        passed=validation.passed,
        current_source_git_commit=validation.current_source_git_commit,
        manifest_git_commit=validation.manifest_git_commit,
    )
    if not validation.passed:
        raise ValueError(f"Chapter 10A foundation validation failed: {validation}")
    return validation


def required_foundation_paths(repo_root: Path) -> list[Path]:
    paths: list[Path] = [
        repo_root / "results" / "reports" / "reproducibility_manifest.json",
        repo_root / "results" / "reports" / "artifact_inventory.json",
        repo_root / "results" / "reports" / "verification_report.md",
        repo_root / "results" / "system_fits" / "phase3_system_fit_manifest.json",
    ]
    for dataset_id in REQUIRED_DATASET_IDS:
        paths.append(repo_root / "datasets" / "manifests" / f"{dataset_id}.json")
        for split in BENCHMARK_SPLITS.values():
            paths.append(repo_root / "datasets" / "processed" / dataset_id / f"{split}.npz")
        for specialist_id in REQUIRED_SPECIALIST_IDS:
            paths.append(repo_root / "results" / "checkpoints" / f"{dataset_id}__{specialist_id}.joblib")
            paths.append(repo_root / "results" / "checkpoints" / f"{dataset_id}__{specialist_id}.metadata.json")
    for config_id in REQUIRED_SYSTEM_CONFIGS:
        paths.append(repo_root / "configs" / "systems" / f"{config_id}.yaml")
    for split_label in ("locked", "audit"):
        paths.append(repo_root / "results" / "metrics" / split_label / "benchmark_metrics_summary.csv")
        paths.append(repo_root / "results" / "metrics" / split_label / "benchmark_run_manifest.json")
    return paths


def verification_report_status(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if "Overall status: `pass`" in text:
        return "pass"
    if "Overall status: `fail`" in text:
        return "fail"
    return "unknown"


def verify_inventory_hashes(repo_root: Path, inventory: dict[str, Any]) -> dict[str, Any]:
    missing: list[str] = []
    mismatches: list[str] = []
    checked = 0
    self_excluded = str(inventory.get("self_excluded_path", "")).replace("\\", "/")
    for artifact in inventory.get("artifacts", []):
        rel_path = str(artifact["path"]).replace("\\", "/")
        if rel_path == self_excluded:
            continue
        path = repo_root / rel_path
        if not path.exists():
            missing.append(rel_path)
            continue
        checked += 1
        actual = hash_file(path)
        expected = str(artifact["sha256"])
        if actual != expected:
            mismatches.append(f"{rel_path}: {actual} != {expected}")
    return {"checked": checked, "missing": missing, "mismatches": mismatches}


def validate_governance_trace_schema(repo_root: Path, *, max_records_per_file: int | None = None) -> dict[str, Any]:
    failures: list[str] = []
    checked = 0
    for split_label in ("locked", "audit"):
        for dataset_id in REQUIRED_DATASET_IDS:
            for system_id in ("veto_mavs", "pure_mavs_gc"):
                path = repo_root / "results" / "traces" / split_label / f"{dataset_id}__{system_id}.traces.jsonl"
                if not path.exists():
                    failures.append(f"missing trace file: {path}")
                    continue
                with path.open("r", encoding="utf-8") as handle:
                    for index, line in enumerate(handle, start=1):
                        if max_records_per_file is not None and index > max_records_per_file:
                            break
                        payload = json.loads(line)
                        missing = [field for field in CH10A_TRACE_FIELDS if field not in payload]
                        if missing:
                            failures.append(f"{path}:{index} missing {missing}")
                        checked += 1
    return {"checked_records": checked, "failures": failures}


def collect_config_hashes(repo_root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for config_id in REQUIRED_SYSTEM_CONFIGS:
        path = repo_root / "configs" / "systems" / f"{config_id}.yaml"
        hashes[str(path.relative_to(repo_root))] = hash_file(path)
    return hashes


def collect_checkpoint_hashes(repo_root: Path) -> dict[str, dict[str, str]]:
    hashes: dict[str, dict[str, str]] = {}
    for dataset_id in REQUIRED_DATASET_IDS:
        dataset_hashes: dict[str, str] = {}
        for specialist_id in REQUIRED_SPECIALIST_IDS:
            checkpoint_path = repo_root / "results" / "checkpoints" / f"{dataset_id}__{specialist_id}.joblib"
            metadata_path = repo_root / "results" / "checkpoints" / f"{dataset_id}__{specialist_id}.metadata.json"
            metadata = read_json(metadata_path)
            dataset_hashes[specialist_id] = str(metadata.get("checkpoint_sha256", hash_file(checkpoint_path)))
        hashes[dataset_id] = dataset_hashes
    return hashes


def collect_split_hashes(repo_root: Path) -> dict[str, dict[str, str]]:
    hashes: dict[str, dict[str, str]] = {}
    for dataset_id in REQUIRED_DATASET_IDS:
        manifest = read_json(repo_root / "datasets" / "manifests" / f"{dataset_id}.json")
        split_hashes: dict[str, str] = {}
        for split in BENCHMARK_SPLITS.values():
            split_hashes[split] = str(manifest["hashes"]["processed_splits"][split]["artifact_sha256"])
        hashes[dataset_id] = split_hashes
    return hashes

