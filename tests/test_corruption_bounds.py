from __future__ import annotations

import numpy as np

from mavs_ch10b.corruptions.registry import build_registry
from tests.test_corruption_determinism import definition_for, synthetic_bundle


def test_all_corruptions_preserve_numeric_bounds_and_row_traceability() -> None:
    registry = build_registry(__import__("pathlib").Path.cwd())
    bundle = synthetic_bundle()
    for family, corruption in registry.items():
        output = corruption.apply(bundle, definition_for(family, corruption.target_space, corruption.config_hash, 1.0, 1001))
        assert np.all(np.isfinite(output.features)), family
        assert np.all((output.probabilities >= 0.0) & (output.probabilities <= 1.0)), family
        assert np.all((output.supports >= -1.0) & (output.supports <= 1.0)), family
        assert set(output.row_ids).issubset(set(bundle.row_ids)), family
        assert output.row_ids.shape[0] <= bundle.row_ids.shape[0], family

