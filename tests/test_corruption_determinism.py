from __future__ import annotations

import numpy as np

from mavs_ch10b.corruptions.base import CorruptionInput, CorruptionRunDefinition, output_bundle_hash
from mavs_ch10b.corruptions.registry import build_registry


def test_stochastic_corruption_is_deterministic_under_fixed_seed() -> None:
    registry = build_registry(__import__("pathlib").Path.cwd())
    bundle = synthetic_bundle()
    corruption = registry["feature_noise"]
    definition = definition_for(corruption.corruption_family, corruption.target_space, corruption.config_hash, level=0.6, seed=1001)
    first = corruption.apply(bundle, definition)
    second = corruption.apply(bundle, definition)
    assert output_bundle_hash(first) == output_bundle_hash(second)


def synthetic_bundle() -> CorruptionInput:
    features = np.arange(60, dtype=np.float64).reshape(10, 6) / 10.0
    probabilities = np.tile(np.array([[0.2, 0.6, 0.8]], dtype=np.float64), (10, 1))
    return CorruptionInput(
        dataset_id="synthetic",
        split="locked_benchmark",
        row_ids=np.arange(10),
        feature_names=tuple(f"f{i}" for i in range(6)),
        specialist_ids=("random_forest", "gradient_boosted_trees", "mlp"),
        features=features,
        y_clean=np.array([0, 1] * 5, dtype=np.int8),
        probabilities=probabilities,
        supports=2.0 * probabilities - 1.0,
    )


def definition_for(family: str, target_space: str, config_hash: str, level: float, seed: int) -> CorruptionRunDefinition:
    return CorruptionRunDefinition(
        dataset_id="synthetic",
        split_label="locked",
        split="locked_benchmark",
        corruption_family=family,
        level=level,
        seed=seed,
        seed_role="primary",
        target_space=target_space,
        corruption_config_hash=config_hash,
        corruption_id=f"synthetic__{family}",
    )

