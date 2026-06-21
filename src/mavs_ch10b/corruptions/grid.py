from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml

from mavs_ch10b.corruptions.base import CorruptionRunDefinition
from mavs_ch10b.corruptions.registry import REQUIRED_CORRUPTION_FAMILIES, build_registry
from mavs_ch10b.verification.hash_utils import console, hash_json


def load_grid_config(repo_root: Path, config_path: Path = Path("configs/corruptions/corruption_grid.yaml")) -> dict[str, Any]:
    resolved = config_path if config_path.is_absolute() else repo_root / config_path
    config = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    if tuple(config["corruption_families"]) != REQUIRED_CORRUPTION_FAMILIES:
        raise ValueError("Corruption grid families must match the required Phase 2 family order")
    # Phase 2 console.log: records corruption grid configuration loading.
    console.log("phase2.corruption.grid_config_loaded", path=str(resolved), families=len(config["corruption_families"]), levels=len(config["levels"]))
    return config


def build_corruption_grid(repo_root: Path, config_path: Path = Path("configs/corruptions/corruption_grid.yaml")) -> list[CorruptionRunDefinition]:
    config = load_grid_config(repo_root, config_path)
    registry = build_registry(repo_root)
    definitions: list[CorruptionRunDefinition] = []
    for dataset_id in config["datasets"]:
        for split_label, split in config["benchmark_splits"].items():
            seed_pairs = seed_pairs_for_split(config, split_label)
            for family in config["corruption_families"]:
                corruption = registry[family]
                for level in config["levels"]:
                    for seed_role, seed in seed_pairs:
                        corruption_id = make_corruption_id(dataset_id, split, family, float(level), int(seed), seed_role)
                        definitions.append(
                            CorruptionRunDefinition(
                                dataset_id=str(dataset_id),
                                split_label=str(split_label),
                                split=str(split),
                                corruption_family=str(family),
                                level=float(level),
                                seed=int(seed),
                                seed_role=str(seed_role),
                                target_space=corruption.target_space,
                                corruption_config_hash=corruption.config_hash,
                                corruption_id=corruption_id,
                            )
                        )
    # Phase 2 console.log: records corruption grid expansion.
    console.log("phase2.corruption.grid_built", definitions=len(definitions), datasets=len(config["datasets"]), families=len(config["corruption_families"]))
    return definitions


def seed_pairs_for_split(config: dict[str, Any], split_label: str) -> list[tuple[str, int]]:
    if split_label == "locked":
        pairs = [("primary", int(seed)) for seed in config["primary_seeds"]]
    elif split_label == "audit":
        pairs = [("audit", int(seed)) for seed in config["audit_seeds"]]
    else:
        raise ValueError(f"Unsupported split label: {split_label}")
    if bool(config.get("include_shadow_verification", True)):
        pairs.extend(("shadow", int(seed)) for seed in config["shadow_verification_seeds"])
    return pairs


def make_corruption_id(dataset_id: str, split: str, family: str, level: float, seed: int, seed_role: str) -> str:
    level_token = f"{level:.2f}".replace(".", "p")
    return f"{dataset_id}__{split}__{family}__level_{level_token}__{seed_role}_{seed}"


def write_grid_manifest(repo_root: Path, definitions: list[CorruptionRunDefinition], config_path: Path = Path("configs/corruptions/corruption_grid.yaml")) -> dict[str, Any]:
    config = load_grid_config(repo_root, config_path)
    output_dir = repo_root / config["manifest_output_dir"]
    manifests_dir = output_dir / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)
    index_records: list[dict[str, Any]] = []
    for definition in definitions:
        payload = definition_manifest_payload(definition)
        family_dir = manifests_dir / definition.corruption_family
        family_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = family_dir / f"{definition.corruption_id}.json"
        manifest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        index_records.append({**payload, "manifest_path": str(manifest_path), "manifest_file_sha256": file_hash_text(manifest_path)})
    csv_path = output_dir / "corruption_manifest_index.csv"
    json_path = output_dir / "corruption_manifest_index.json"
    write_index_csv(csv_path, index_records)
    json_payload = {"schema_version": "1.0", "phase": "phase2", "definitions": index_records}
    json_payload["payload_sha256"] = hash_json(json_payload)
    json_path.write_text(json.dumps(json_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    grid_manifest = {
        "schema_version": "1.0",
        "phase": "phase2",
        "grid_config_hash": hash_json(config),
        "definition_count": len(definitions),
        "datasets": config["datasets"],
        "benchmark_splits": config["benchmark_splits"],
        "corruption_families": config["corruption_families"],
        "levels": config["levels"],
        "primary_seeds": config["primary_seeds"],
        "audit_seeds": config["audit_seeds"],
        "shadow_verification_seeds": config["shadow_verification_seeds"],
        "index_csv_path": str(csv_path),
        "index_csv_sha256": file_hash_text(csv_path),
        "index_json_path": str(json_path),
        "index_json_sha256": file_hash_text(json_path),
    }
    grid_manifest["manifest_payload_sha256"] = hash_json(grid_manifest)
    grid_manifest_path = output_dir / "corruption_grid_manifest.json"
    grid_manifest_path.write_text(json.dumps(grid_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    grid_manifest["manifest_path"] = str(grid_manifest_path)
    grid_manifest["manifest_file_sha256"] = file_hash_text(grid_manifest_path)
    # Phase 2 console.log: records corruption grid manifest persistence.
    console.log(
        "phase2.corruption.grid_manifest_written",
        path=str(grid_manifest_path),
        definitions=len(definitions),
        index_csv=str(csv_path),
    )
    return grid_manifest


def definition_manifest_payload(definition: CorruptionRunDefinition) -> dict[str, Any]:
    payload = {
        "schema_version": "1.0",
        "phase": "phase2",
        "dataset_id": definition.dataset_id,
        "split_label": definition.split_label,
        "split": definition.split,
        "corruption_family": definition.corruption_family,
        "corruption_id": definition.corruption_id,
        "corruption_level": definition.level,
        "corruption_seed": definition.seed,
        "seed_role": definition.seed_role,
        "target_space": definition.target_space,
        "corruption_config_hash": definition.corruption_config_hash,
        "random_seed_hash": hash_json({"seed": definition.seed, "corruption_id": definition.corruption_id}),
    }
    payload["definition_manifest_hash"] = hash_json(payload)
    return payload


def write_index_csv(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(records[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    # Phase 2 console.log: records corruption manifest index CSV persistence.
    console.log("phase2.corruption.index_csv_written", path=str(path), rows=len(records))


def file_hash_text(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()
