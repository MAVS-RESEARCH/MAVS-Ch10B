from __future__ import annotations

import csv
import json
from pathlib import Path

import yaml

from mavs_ch10b.adapters.ch10a_artifacts import collect_checkpoint_hashes, collect_config_hashes, collect_split_hashes
from mavs_ch10b.corruptions.manifest import REQUIRED_APPLIED_MANIFEST_FIELDS, build_applied_manifest
from mavs_ch10b.corruptions.registry import build_registry
from mavs_ch10b.verification.hash_utils import hash_file
from tests.test_corruption_determinism import definition_for, synthetic_bundle


def test_applied_manifest_contains_required_hash_fields() -> None:
    registry = build_registry(Path.cwd())
    bundle = synthetic_bundle()
    corruption = registry["specialist_failure"]
    definition = definition_for("specialist_failure", corruption.target_space, corruption.config_hash, 1.0, 1001)
    output = corruption.apply(bundle, definition)
    manifest = build_applied_manifest(corruption, bundle, output)
    assert set(REQUIRED_APPLIED_MANIFEST_FIELDS).issubset(manifest)
    assert manifest["failed_specialists"]
    assert manifest["input_bundle_hash"] != manifest["output_bundle_hash"]


def test_generated_grid_manifest_and_index_are_complete() -> None:
    repo_root = Path.cwd()
    grid_manifest_path = repo_root / "results" / "corruption_manifests" / "corruption_grid_manifest.json"
    index_path = repo_root / "results" / "corruption_manifests" / "corruption_manifest_index.csv"
    assert grid_manifest_path.exists()
    assert index_path.exists()
    grid_manifest = yaml.safe_load(grid_manifest_path.read_text(encoding="utf-8"))
    assert grid_manifest["definition_count"] == 2880
    assert hash_file(index_path) == grid_manifest["index_csv_sha256"]
    with index_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 2880


def test_ch10a_artifact_hashes_remain_unchanged_after_phase2() -> None:
    repo_root = Path.cwd()
    import_manifest = json.loads((repo_root / "results" / "baseline_import" / "ch10a_import_manifest.json").read_text(encoding="utf-8"))
    ch10a_root = Path(import_manifest["local_artifact_path"])
    assert hash_file(Path(import_manifest["artifact_inventory_path"])) == import_manifest["artifact_inventory_sha256"]
    assert hash_file(Path(import_manifest["reproducibility_manifest_path"])) == import_manifest["reproducibility_manifest_sha256"]
    assert hash_file(Path(import_manifest["verification_report_path"])) == import_manifest["verification_report_sha256"]
    assert collect_checkpoint_hashes(ch10a_root) == import_manifest["checkpoint_hashes"]
    assert collect_config_hashes(ch10a_root) == import_manifest["config_hashes"]
    assert collect_split_hashes(ch10a_root) == import_manifest["split_hashes"]
    assert import_manifest["validation"]["inventory_mismatches"] == []
    assert import_manifest["validation"]["inventory_missing"] == []
