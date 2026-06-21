from __future__ import annotations

import abc
import hashlib
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import numpy as np

from mavs_ch10b.verification.hash_utils import console, hash_json


@dataclass(frozen=True)
class CorruptionInput:
    dataset_id: str
    split: str
    row_ids: np.ndarray
    feature_names: tuple[str, ...]
    specialist_ids: tuple[str, ...]
    features: np.ndarray
    y_clean: np.ndarray
    probabilities: np.ndarray
    supports: np.ndarray

    def validate(self) -> None:
        rows = self.features.shape[0]
        if self.row_ids.shape[0] != rows or self.y_clean.shape[0] != rows:
            raise ValueError("Feature, row id, and label rows must align")
        if self.probabilities.shape != self.supports.shape:
            raise ValueError("Probability and support matrices must align")
        if self.probabilities.shape[0] != rows:
            raise ValueError("Score rows must align with feature rows")
        if self.probabilities.shape[1] != len(self.specialist_ids):
            raise ValueError("Score columns must align with specialist ids")
        if self.features.shape[1] != len(self.feature_names):
            raise ValueError("Feature columns must align with feature names")


@dataclass(frozen=True)
class CorruptionRunDefinition:
    dataset_id: str
    split_label: str
    split: str
    corruption_family: str
    level: float
    seed: int
    seed_role: str
    target_space: str
    corruption_config_hash: str
    corruption_id: str


@dataclass(frozen=True)
class CorruptionOutput:
    definition: CorruptionRunDefinition
    row_ids: np.ndarray
    features: np.ndarray
    y_clean: np.ndarray
    y_observed: np.ndarray
    probabilities: np.ndarray
    supports: np.ndarray
    changed_mask: np.ndarray | None
    failed_specialists: tuple[str, ...]
    distribution_shift_descriptor: dict[str, Any]
    metadata: dict[str, Any]

    def validate(self) -> None:
        rows = self.row_ids.shape[0]
        if self.features.shape[0] != rows or self.y_clean.shape[0] != rows or self.y_observed.shape[0] != rows:
            raise ValueError("Output feature, row id, and label rows must align")
        if self.probabilities.shape != self.supports.shape:
            raise ValueError("Output probability and support matrices must align")
        if self.probabilities.shape[0] != rows:
            raise ValueError("Output score rows must align with output rows")
        if not np.all(np.isfinite(self.features)):
            raise ValueError("Corrupted features contain non-finite values")
        if not np.all((self.probabilities >= 0.0) & (self.probabilities <= 1.0)):
            raise ValueError("Corrupted probabilities are outside [0, 1]")
        if not np.all((self.supports >= -1.0) & (self.supports <= 1.0)):
            raise ValueError("Corrupted supports are outside [-1, 1]")


class Corruption(abc.ABC):
    corruption_family: str
    target_space: str

    def __init__(self, config: dict[str, Any]):
        self.config = dict(config)
        self.corruption_family = str(config["corruption_family"])
        self.target_space = str(config["target_space"])
        self.stochastic = bool(config.get("stochastic", True))
        self.parameters = dict(config.get("parameters", {}))
        self.config_hash = hash_json(self.config)

    def corruption_id(self, definition: CorruptionRunDefinition) -> str:
        return definition.corruption_id

    def apply(self, bundle: CorruptionInput, definition: CorruptionRunDefinition) -> CorruptionOutput:
        validate_level(definition.level)
        bundle.validate()
        # Phase 2 console.log: records corruption application dispatch.
        console.log(
            "phase2.corruption.apply_start",
            family=self.corruption_family,
            dataset_id=bundle.dataset_id,
            split=bundle.split,
            level=definition.level,
            seed=definition.seed,
        )
        output = self._apply(bundle, definition)
        output.validate()
        # Phase 2 console.log: records corruption application completion.
        console.log(
            "phase2.corruption.apply_complete",
            family=self.corruption_family,
            dataset_id=bundle.dataset_id,
            split=bundle.split,
            rows=int(output.row_ids.shape[0]),
            output_hash=output_bundle_hash(output),
        )
        return output

    @abc.abstractmethod
    def _apply(self, bundle: CorruptionInput, definition: CorruptionRunDefinition) -> CorruptionOutput:
        raise NotImplementedError

    def manifest(self, bundle: CorruptionInput, output: CorruptionOutput) -> dict[str, Any]:
        manifest = {
            "schema_version": "1.0",
            "phase": "phase2",
            "dataset_id": output.definition.dataset_id,
            "split_label": output.definition.split_label,
            "split": output.definition.split,
            "corruption_family": output.definition.corruption_family,
            "corruption_id": output.definition.corruption_id,
            "corruption_level": output.definition.level,
            "corruption_seed": output.definition.seed,
            "seed_role": output.definition.seed_role,
            "target_space": output.definition.target_space,
            "corruption_config_hash": output.definition.corruption_config_hash,
            "random_seed_hash": hash_json({"seed": output.definition.seed, "corruption_id": output.definition.corruption_id}),
            "input_bundle_hash": input_bundle_hash(bundle),
            "output_bundle_hash": output_bundle_hash(output),
            "feature_mask_hash": mask_hash(output.changed_mask),
            "score_hash_clean": array_hash(bundle.probabilities),
            "score_hash_corrupted": array_hash(output.probabilities),
            "y_clean_hash": array_hash(output.y_clean),
            "y_observed_hash": array_hash(output.y_observed),
            "failed_specialists": list(output.failed_specialists),
            "distribution_shift_descriptor": output.distribution_shift_descriptor,
            "metadata": output.metadata,
        }
        manifest["corruption_manifest_hash"] = hash_json(manifest)
        # Phase 2 console.log: records applied corruption manifest construction.
        console.log("phase2.corruption.manifest_built", corruption_id=output.definition.corruption_id, manifest_hash=manifest["corruption_manifest_hash"])
        return manifest

    def _base_output(self, bundle: CorruptionInput, definition: CorruptionRunDefinition, **changes: Any) -> CorruptionOutput:
        output = CorruptionOutput(
            definition=definition,
            row_ids=np.array(bundle.row_ids, copy=True),
            features=np.array(bundle.features, copy=True),
            y_clean=np.array(bundle.y_clean, copy=True),
            y_observed=np.array(bundle.y_clean, copy=True),
            probabilities=np.array(bundle.probabilities, copy=True),
            supports=np.array(bundle.supports, copy=True),
            changed_mask=None,
            failed_specialists=(),
            distribution_shift_descriptor={},
            metadata={},
        )
        return replace(output, **changes)


def validate_level(level: float) -> None:
    if level < 0.0 or level > 1.0:
        raise ValueError(f"Corruption level must be in [0, 1], got {level}")


def deterministic_rng(definition: CorruptionRunDefinition) -> np.random.Generator:
    seed_material = f"{definition.dataset_id}|{definition.split}|{definition.corruption_family}|{definition.level:.8f}|{definition.seed}|{definition.seed_role}"
    seed = int(hashlib.sha256(seed_material.encode("utf-8")).hexdigest()[:16], 16) % (2**32)
    # Phase 2 console.log: records deterministic RNG creation for a corruption run.
    console.log("phase2.corruption.rng_created", corruption_id=definition.corruption_id, derived_seed=seed)
    return np.random.default_rng(seed)


def array_hash(array: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(array)
    digest = hashlib.sha256()
    digest.update(str(contiguous.shape).encode("utf-8"))
    digest.update(str(contiguous.dtype).encode("utf-8"))
    digest.update(contiguous.tobytes())
    return digest.hexdigest()


def mask_hash(mask: np.ndarray | None) -> str | None:
    if mask is None:
        return None
    return array_hash(mask.astype(np.int8))


def input_bundle_hash(bundle: CorruptionInput) -> str:
    return hash_json(
        {
            "dataset_id": bundle.dataset_id,
            "split": bundle.split,
            "row_ids": array_hash(bundle.row_ids),
            "feature_names": list(bundle.feature_names),
            "specialist_ids": list(bundle.specialist_ids),
            "features": array_hash(bundle.features),
            "y_clean": array_hash(bundle.y_clean),
            "probabilities": array_hash(bundle.probabilities),
            "supports": array_hash(bundle.supports),
        }
    )


def output_bundle_hash(output: CorruptionOutput) -> str:
    return hash_json(
        {
            "row_ids": array_hash(output.row_ids),
            "features": array_hash(output.features),
            "y_clean": array_hash(output.y_clean),
            "y_observed": array_hash(output.y_observed),
            "probabilities": array_hash(output.probabilities),
            "supports": array_hash(output.supports),
            "changed_mask": mask_hash(output.changed_mask),
            "failed_specialists": list(output.failed_specialists),
            "distribution_shift_descriptor": output.distribution_shift_descriptor,
            "metadata": output.metadata,
        }
    )


def supports_from_probabilities(probabilities: np.ndarray) -> np.ndarray:
    return np.clip(2.0 * probabilities - 1.0, -1.0, 1.0)

