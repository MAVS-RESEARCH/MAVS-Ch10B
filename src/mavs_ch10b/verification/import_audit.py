from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from mavs_ch10b.adapters.ch10a_artifacts import (
    REQUIRED_DATASET_IDS,
    REQUIRED_SPECIALIST_IDS,
    REQUIRED_SYSTEM_IDS,
    validate_ch10a_foundation,
)
from mavs_ch10b.adapters.ch10a_source import locate_ch10a_source
from mavs_ch10b.verification.hash_utils import console, hash_file, hash_json, write_json


FORBIDDEN_TRAINING_TOKENS: tuple[str, ...] = (
    "train_specialists.py",
    "prepare_datasets.py",
    "reproduce_all.py",
    "fit_static_weights",
)


def validate_no_training_command(command_line: list[str]) -> None:
    lowered = " ".join(command_line).lower()
    forbidden = [token for token in FORBIDDEN_TRAINING_TOKENS if token.lower() in lowered]
    # Phase 1 console.log: records no-retraining command guard evaluation.
    console.log("phase1.import_audit.no_training_command_checked", command_line=command_line, forbidden=forbidden)
    if forbidden:
        raise ValueError(f"Phase 1 refuses training or reconstruction commands: {forbidden}")


def run_import_audit(repo_root: Path, config_path: Path) -> dict[str, Any]:
    validate_no_training_command(["import_ch10a_foundation.py"])
    output_dir = repo_root / "results" / "baseline_import"
    output_dir.mkdir(parents=True, exist_ok=True)
    # Phase 1 console.log: records Chapter 10A foundation import audit dispatch.
    console.log("phase1.import_audit.dispatch", repo_root=str(repo_root), output_dir=str(output_dir), config=str(config_path))
    source = locate_ch10a_source(repo_root, config_path)
    validation = validate_ch10a_foundation(
        source,
        verify_inventory=bool(source.config.get("verify_artifact_inventory_hashes", True)),
        verify_trace_schema=bool(source.config.get("verify_governance_trace_schema", True)),
    )
    manifest_path = output_dir / "ch10a_import_manifest.json"
    report_path = output_dir / "ch10a_import_report.md"
    artifact_inventory_path = source.repo_root / str(source.config["artifact_inventory_path"])
    reproducibility_manifest_path = source.repo_root / str(source.config["reproducibility_manifest_path"])
    verification_report_path = source.repo_root / str(source.config["verification_report_path"])
    manifest = {
        "schema_version": "1.0",
        "phase": "phase1",
        "source_repo_url": source.source_repo_url,
        "local_artifact_path": str(source.repo_root),
        "source_git_commit": validation.current_source_git_commit,
        "manifest_git_commit": validation.manifest_git_commit,
        "artifact_inventory_path": str(artifact_inventory_path),
        "artifact_inventory_sha256": hash_file(artifact_inventory_path),
        "reproducibility_manifest_path": str(reproducibility_manifest_path),
        "reproducibility_manifest_sha256": hash_file(reproducibility_manifest_path),
        "verification_report_path": str(verification_report_path),
        "verification_report_sha256": hash_file(verification_report_path),
        "verification_report_status": validation.verification_report_status,
        "imported_dataset_ids": list(REQUIRED_DATASET_IDS),
        "imported_specialist_ids": list(REQUIRED_SPECIALIST_IDS),
        "imported_system_ids": list(REQUIRED_SYSTEM_IDS),
        "checkpoint_hashes": validation.checkpoint_hashes,
        "config_hashes": validation.config_hashes,
        "split_hashes": validation.split_hashes,
        "validation": asdict(validation),
    }
    write_import_report(report_path, manifest)
    manifest["report_path"] = str(report_path)
    manifest["report_sha256"] = hash_file(report_path)
    manifest["manifest_payload_sha256"] = hash_json(manifest)
    write_json(manifest_path, manifest)
    manifest_file_sha256 = hash_file(manifest_path)
    # Phase 1 console.log: records Chapter 10A import manifest completion.
    console.log(
        "phase1.import_audit.complete",
        manifest_path=str(manifest_path),
        report_path=str(report_path),
        manifest_file_sha256=manifest_file_sha256,
        report_sha256=manifest["report_sha256"],
    )
    manifest["manifest_file_sha256"] = manifest_file_sha256
    return manifest


def write_import_report(path: Path, manifest: dict[str, Any]) -> None:
    validation = manifest["validation"]
    lines = [
        "# Chapter 10B Phase 1 Import Report",
        "",
        f"Chapter 10A source: `{manifest['local_artifact_path']}`",
        f"Source repository: `{manifest['source_repo_url']}`",
        f"Current source git commit: `{manifest['source_git_commit']}`",
        f"Manifest git commit: `{manifest['manifest_git_commit']}`",
        f"Chapter 10A verification status: `{manifest['verification_report_status']}`",
        "",
        "## Imported Foundation",
        "",
        f"Datasets: `{len(manifest['imported_dataset_ids'])}`",
        f"Specialists: `{len(manifest['imported_specialist_ids'])}`",
        f"Systems: `{len(manifest['imported_system_ids'])}`",
        f"Required files checked: `{validation['required_files_checked']}`",
        f"Inventory artifacts checked: `{validation['inventory_checked_artifacts']}`",
        f"Governance trace records checked: `{validation['trace_records_checked']}`",
        "",
        "## Result",
        "",
        "Phase 1 import status: `pass`.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # Phase 1 console.log: records Chapter 10A import report persistence.
    console.log("phase1.import_audit.report_written", path=str(path))
