from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import numpy as np

from mavs_ch10b.adapters.ch10a_source import Chapter10ASource, ensure_ch10a_importable
from mavs_ch10b.corruptions.base import (
    CorruptionInput,
    CorruptionOutput,
    CorruptionRunDefinition,
    array_hash,
    input_bundle_hash,
    mask_hash,
    output_bundle_hash,
)
from mavs_ch10b.corruptions.manifest import build_applied_manifest, write_applied_manifest
from mavs_ch10b.stress.cache import CleanBenchmarkBundle, StressCache
from mavs_ch10b.verification.hash_utils import console, hash_file, hash_json


@dataclass(frozen=True)
class PreparedCorruptionBundle:
    definition: CorruptionRunDefinition
    bundle: Any
    corruption_output: CorruptionOutput
    applied_manifest: dict[str, Any]
    applied_manifest_path: Path
    applied_manifest_file_sha256: str
    metadata: dict[str, Any]


def prepare_corrupted_bundle(
    *,
    source: Chapter10ASource,
    cache: StressCache,
    clean: CleanBenchmarkBundle,
    corruption: Any,
    definition: CorruptionRunDefinition,
    applied_manifest_dir: Path,
) -> PreparedCorruptionBundle:
    # Phase 3 console.log: records corruption preparation dispatch before system execution.
    console.log(
        "phase3.executor.prepare_corruption_start",
        dataset_id=definition.dataset_id,
        split=definition.split,
        corruption_id=definition.corruption_id,
        target_space=definition.target_space,
    )
    corruption_input = CorruptionInput(
        dataset_id=definition.dataset_id,
        split=definition.split,
        row_ids=np.asarray(clean.specialist_bundle.row_ids),
        feature_names=clean.feature_names,
        specialist_ids=tuple(clean.specialist_bundle.model_ids),
        features=clean.features,
        y_clean=np.asarray(clean.specialist_bundle.labels),
        probabilities=np.asarray(clean.specialist_bundle.probabilities),
        supports=np.asarray(clean.specialist_bundle.supports),
    )
    clean_input_hash = array_hash(clean.features)
    clean_score_hash = array_hash(clean.specialist_bundle.probabilities)
    output = corruption.apply(corruption_input, definition)
    probabilities, supports, checkpoint_hashes = _scores_for_corruption(cache, clean, output, definition)
    output = replace(output, probabilities=probabilities, supports=supports)
    stress_bundle = _build_ch10a_bundle(source, clean, output, checkpoint_hashes)
    applied_manifest = build_applied_manifest(corruption, corruption_input, output)
    applied_manifest_path = applied_manifest_dir / definition.corruption_family / f"{definition.corruption_id}.yaml"
    write_applied_manifest(applied_manifest_path, applied_manifest)
    metadata = {
        "clean_input_bundle_hash": input_bundle_hash(corruption_input),
        "corrupted_input_bundle_hash": output_bundle_hash(output),
        "input_hash_clean": clean_input_hash,
        "input_hash_corrupted": array_hash(output.features),
        "score_hash_clean": clean_score_hash,
        "score_hash_corrupted": array_hash(output.probabilities),
        "feature_mask_hash": mask_hash(output.changed_mask),
        "failed_specialists": list(output.failed_specialists),
        "distribution_shift_descriptor": output.distribution_shift_descriptor,
        "applied_corruption_manifest_hash": applied_manifest["corruption_manifest_hash"],
        "applied_corruption_manifest_file_sha256": hash_file(applied_manifest_path),
        "applied_corruption_manifest_path": str(applied_manifest_path),
        "corrupted_rows": int(output.row_ids.shape[0]),
        "specialist_ids": list(stress_bundle.model_ids),
        "specialist_count": int(len(stress_bundle.model_ids)),
    }
    # Phase 3 console.log: records corruption preparation completion before shared system execution.
    console.log(
        "phase3.executor.prepare_corruption_complete",
        corruption_id=definition.corruption_id,
        rows=metadata["corrupted_rows"],
        corrupted_bundle_hash=metadata["corrupted_input_bundle_hash"],
        manifest_hash=metadata["applied_corruption_manifest_hash"],
    )
    return PreparedCorruptionBundle(
        definition=definition,
        bundle=stress_bundle,
        corruption_output=output,
        applied_manifest=applied_manifest,
        applied_manifest_path=applied_manifest_path,
        applied_manifest_file_sha256=metadata["applied_corruption_manifest_file_sha256"],
        metadata=metadata,
    )


def execute_system(system: Any, prepared: PreparedCorruptionBundle) -> Any:
    # Phase 3 console.log: records system execution dispatch on a shared corrupted bundle.
    console.log(
        "phase3.executor.system_start",
        dataset_id=prepared.definition.dataset_id,
        split=prepared.definition.split,
        system_id=system.system_id,
        corruption_id=prepared.definition.corruption_id,
        bundle_hash=prepared.metadata["corrupted_input_bundle_hash"],
    )
    output = system.run(prepared.bundle)
    if len(output.decisions) != prepared.corruption_output.row_ids.shape[0]:
        raise ValueError(f"System row count mismatch for {system.system_id} and {prepared.definition.corruption_id}")
    # Phase 3 console.log: records system execution completion on a shared corrupted bundle.
    console.log(
        "phase3.executor.system_complete",
        dataset_id=prepared.definition.dataset_id,
        split=prepared.definition.split,
        system_id=system.system_id,
        corruption_id=prepared.definition.corruption_id,
        rows=int(len(output.decisions)),
        trace_rows=int(len(output.traces)),
    )
    return output


def system_output_hash(output: Any) -> str:
    return hash_json(
        {
            "dataset_id": output.dataset_id,
            "split": output.split,
            "system_id": output.system_id,
            "probabilities": array_hash(np.asarray(output.probabilities)),
            "decisions": array_hash(np.asarray(output.decisions)),
            "trace_rows": len(output.traces),
        }
    )


def _scores_for_corruption(
    cache: StressCache,
    clean: CleanBenchmarkBundle,
    output: CorruptionOutput,
    definition: CorruptionRunDefinition,
) -> tuple[np.ndarray, np.ndarray, dict[str, str]]:
    if definition.target_space == "features" and float(definition.level) > 0.0:
        return cache.predict_specialists(definition.dataset_id, output.features)
    return (
        np.asarray(output.probabilities, dtype=np.float64),
        np.asarray(output.supports, dtype=np.float64),
        dict(clean.specialist_bundle.checkpoint_hashes),
    )


def _build_ch10a_bundle(source: Chapter10ASource, clean: CleanBenchmarkBundle, output: CorruptionOutput, checkpoint_hashes: dict[str, str]) -> Any:
    ensure_ch10a_importable(source)
    from mavs_ch10a.systems.base import SpecialistOutputBundle

    return SpecialistOutputBundle(
        dataset_id=output.definition.dataset_id,
        split=output.definition.split,
        row_ids=np.asarray(output.row_ids),
        labels=np.asarray(output.y_clean),
        model_ids=tuple(clean.specialist_bundle.model_ids),
        probabilities=np.asarray(output.probabilities, dtype=np.float64),
        supports=np.asarray(output.supports, dtype=np.float64),
        checkpoint_hashes=checkpoint_hashes,
        processed_split_sha256=str(clean.specialist_bundle.processed_split_sha256),
        config_hash=hash_json(
            {
                "dataset_id": output.definition.dataset_id,
                "split": output.definition.split,
                "corruption_id": output.definition.corruption_id,
                "probabilities": array_hash(np.asarray(output.probabilities)),
                "supports": array_hash(np.asarray(output.supports)),
                "row_ids": array_hash(np.asarray(output.row_ids)),
            }
        ),
    )
