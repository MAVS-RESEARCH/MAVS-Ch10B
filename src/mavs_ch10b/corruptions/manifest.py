from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from mavs_ch10b.corruptions.base import Corruption, CorruptionInput, CorruptionOutput
from mavs_ch10b.verification.hash_utils import console, hash_json


REQUIRED_APPLIED_MANIFEST_FIELDS: tuple[str, ...] = (
    "schema_version",
    "phase",
    "dataset_id",
    "split",
    "corruption_family",
    "corruption_id",
    "corruption_level",
    "corruption_seed",
    "target_space",
    "corruption_config_hash",
    "random_seed_hash",
    "input_bundle_hash",
    "output_bundle_hash",
    "score_hash_clean",
    "score_hash_corrupted",
    "y_clean_hash",
    "y_observed_hash",
    "failed_specialists",
    "distribution_shift_descriptor",
    "corruption_manifest_hash",
)


def build_applied_manifest(corruption: Corruption, bundle: CorruptionInput, output: CorruptionOutput) -> dict[str, Any]:
    manifest = corruption.manifest(bundle, output)
    missing = [field for field in REQUIRED_APPLIED_MANIFEST_FIELDS if field not in manifest]
    if missing:
        raise ValueError(f"Applied corruption manifest missing fields: {missing}")
    # Phase 2 console.log: records applied manifest schema validation.
    console.log("phase2.corruption.applied_manifest_validated", corruption_id=manifest["corruption_id"], fields=len(manifest))
    return manifest


def write_applied_manifest(path: Path, manifest: dict[str, Any]) -> None:
    payload = dict(manifest)
    payload["file_payload_sha256"] = hash_json(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=True), encoding="utf-8")
    # Phase 2 console.log: records applied corruption manifest persistence.
    console.log("phase2.corruption.applied_manifest_written", path=str(path), corruption_id=manifest["corruption_id"])

