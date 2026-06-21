from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

from mavs_ch10b.adapters.ch10a_artifacts import REQUIRED_SYSTEM_IDS
from mavs_ch10b.adapters.ch10a_source import locate_ch10a_source
from mavs_ch10b.adapters.ch10a_systems import build_comparison_systems, load_frozen_manifest
from mavs_ch10b.corruptions.grid import build_corruption_grid
from mavs_ch10b.corruptions.registry import build_registry
from mavs_ch10b.stress.cache import StressCache
from mavs_ch10b.stress.run_manifest import build_aggregate_rows, enforce_final_mode_controls, write_run_artifacts
from mavs_ch10b.stress.system_executor import execute_system, prepare_corrupted_bundle, system_output_hash
from mavs_ch10b.stress.trace_writer import write_governance_traces, write_prediction_output
from mavs_ch10b.verification.hash_utils import console
from mavs_ch10b.verification.import_audit import validate_no_training_command


def load_experiment_config(repo_root: Path, config_path: Path) -> dict[str, Any]:
    resolved = config_path if config_path.is_absolute() else repo_root / config_path
    config = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    required = {"experiment_id", "run_id", "run_mode", "split_label", "systems", "governance_systems", "output"}
    missing = required - set(config)
    if missing:
        raise ValueError(f"Stress experiment config missing keys {sorted(missing)}: {resolved}")
    if tuple(config["systems"]) != REQUIRED_SYSTEM_IDS:
        raise ValueError(f"Phase 3 system list must match required systems: {config['systems']}")
    # Phase 3 console.log: records stress experiment configuration loading.
    console.log("phase3.run_matrix.config_loaded", path=str(resolved), run_id=config["run_id"], split_label=config["split_label"])
    return config


def run_stress_matrix(
    *,
    repo_root: Path,
    config_path: Path,
    run_id: str | None = None,
    max_definitions: int | None = None,
    command_line: list[str] | None = None,
) -> dict[str, Any]:
    validate_no_training_command(command_line or sys.argv)
    config = load_experiment_config(repo_root, config_path)
    if run_id is not None:
        config = {**config, "run_id": run_id}
    run_id_value = str(config["run_id"])
    enforce_final_mode_controls(repo_root, config)
    source = locate_ch10a_source(repo_root, Path(config["ch10a_source_config"]))
    registry = build_registry(repo_root)
    definitions = [definition for definition in build_corruption_grid(repo_root, Path(config["corruption_grid_config"])) if definition.split_label == config["split_label"]]
    if max_definitions is not None:
        definitions = definitions[:max_definitions]
    if not definitions:
        raise ValueError(f"No corruption definitions selected for split label {config['split_label']}")
    # Phase 3 console.log: records stress matrix dispatch.
    console.log(
        "phase3.run_matrix.dispatch",
        run_id=run_id_value,
        run_mode=config["run_mode"],
        split_label=config["split_label"],
        definitions=len(definitions),
        systems=len(config["systems"]),
    )

    stress_root = repo_root / str(config["output"]["stress_runs_dir"])
    trace_root = repo_root / str(config["output"]["corruption_traces_dir"])
    prediction_root = stress_root / run_id_value / str(config["output"]["predictions_subdir"])
    applied_manifest_dir = stress_root / run_id_value / str(config["output"]["applied_manifests_subdir"])
    trace_run_root = trace_root / run_id_value / str(config["output"]["traces_subdir"])
    prediction_records: list[dict[str, Any]] = []
    trace_records: list[dict[str, Any]] = []
    cache = StressCache(source)
    frozen_manifest = load_frozen_manifest(source)
    system_cache: dict[str, tuple[Any, ...]] = {}

    for definition_index, definition in enumerate(definitions, start=1):
        corruption = registry[definition.corruption_family]
        clean = cache.clean_benchmark_bundle(definition.dataset_id, definition.split)
        prepared = prepare_corrupted_bundle(
            source=source,
            cache=cache,
            clean=clean,
            corruption=corruption,
            definition=definition,
            applied_manifest_dir=applied_manifest_dir,
        )
        systems = system_cache.get(definition.dataset_id)
        if systems is None:
            systems = build_comparison_systems(source, definition.dataset_id, frozen_manifest)
            system_cache[definition.dataset_id] = systems
        # Phase 3 console.log: records one corruption cell dispatch across all comparison systems.
        console.log(
            "phase3.run_matrix.definition_start",
            run_id=run_id_value,
            definition_index=definition_index,
            definitions=len(definitions),
            corruption_id=definition.corruption_id,
            rows=prepared.metadata["corrupted_rows"],
        )
        for system in systems:
            output = execute_system(system, prepared)
            prediction_path = prediction_root / system.system_id / definition.corruption_family / f"{definition.corruption_id}.npz"
            prediction_artifact = write_prediction_output(prediction_path, output, prepared)
            base_record = _base_record(run_id_value, config, definition, system.system_id, prepared)
            trace_artifact = {
                "trace_path": "",
                "trace_sha256": "",
                "trace_rows": 0,
                "trace_required": system.system_id in set(config["governance_systems"]),
                "trace_format": "",
                "trace_schema_hash": "",
                "specialist_count": prepared.metadata["specialist_count"],
            }
            if system.system_id in set(config["governance_systems"]):
                trace_path = trace_run_root / system.system_id / definition.corruption_family / f"{definition.corruption_id}.npz"
                trace_artifact = {**trace_artifact, **write_governance_traces(trace_path, output, prepared)}
                trace_records.append({**base_record, **trace_artifact})
            prediction_records.append(
                {
                    **base_record,
                    **prediction_artifact,
                    **trace_artifact,
                    "system_output_hash": system_output_hash(output),
                    "decision_hash": prediction_artifact["prediction_payload_hash"],
                }
            )
        # Phase 3 console.log: records one corruption cell completion across all comparison systems.
        console.log("phase3.run_matrix.definition_complete", run_id=run_id_value, corruption_id=definition.corruption_id, systems=len(systems))

    aggregate_records = build_aggregate_rows(prediction_records)
    manifest = write_run_artifacts(
        repo_root=repo_root,
        run_id=run_id_value,
        config_path=config_path,
        config=config,
        command_line=command_line or sys.argv,
        prediction_records=prediction_records,
        trace_records=trace_records,
        aggregate_records=aggregate_records,
    )
    # Phase 3 console.log: records stress matrix completion.
    console.log(
        "phase3.run_matrix.complete",
        run_id=run_id_value,
        system_runs=manifest["system_run_count"],
        prediction_rows=manifest["prediction_rows"],
        trace_rows=manifest["trace_rows"],
    )
    return manifest


def _base_record(run_id: str, config: dict[str, Any], definition: Any, system_id: str, prepared: Any) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "run_mode": config.get("run_mode", "exploratory"),
        "split_label": definition.split_label,
        "split": definition.split,
        "dataset_id": definition.dataset_id,
        "system_id": system_id,
        "corruption_family": definition.corruption_family,
        "corruption_id": definition.corruption_id,
        "corruption_level": definition.level,
        "corruption_seed": definition.seed,
        "seed_role": definition.seed_role,
        "corruption_target_space": definition.target_space,
        "corruption_config_hash": definition.corruption_config_hash,
        "corruption_manifest_hash": prepared.metadata["applied_corruption_manifest_hash"],
        "applied_corruption_manifest_path": prepared.metadata["applied_corruption_manifest_path"],
        "applied_corruption_manifest_file_sha256": prepared.metadata["applied_corruption_manifest_file_sha256"],
        "clean_input_bundle_hash": prepared.metadata["clean_input_bundle_hash"],
        "corrupted_input_bundle_hash": prepared.metadata["corrupted_input_bundle_hash"],
        "input_hash_clean": prepared.metadata["input_hash_clean"],
        "input_hash_corrupted": prepared.metadata["input_hash_corrupted"],
        "score_hash_clean": prepared.metadata["score_hash_clean"],
        "score_hash_corrupted": prepared.metadata["score_hash_corrupted"],
        "feature_mask_hash": prepared.metadata["feature_mask_hash"],
        "failed_specialists": "|".join(prepared.metadata["failed_specialists"]),
        "distribution_shift_descriptor": yaml.safe_dump(prepared.metadata["distribution_shift_descriptor"], sort_keys=True).strip(),
        "specialist_ids": "|".join(prepared.metadata["specialist_ids"]),
        "specialist_count": prepared.metadata["specialist_count"],
        "corrupted_rows": prepared.metadata["corrupted_rows"],
    }
