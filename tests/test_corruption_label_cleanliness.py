from __future__ import annotations

import numpy as np

from mavs_ch10b.corruptions.registry import build_registry
from tests.test_corruption_determinism import definition_for, synthetic_bundle


def test_label_noise_preserves_clean_labels_and_changes_observed_labels() -> None:
    registry = build_registry(__import__("pathlib").Path.cwd())
    bundle = synthetic_bundle()
    corruption = registry["label_noise"]
    output = corruption.apply(bundle, definition_for("label_noise", corruption.target_space, corruption.config_hash, 1.0, 1001))
    assert np.array_equal(output.y_clean, bundle.y_clean)
    assert not np.array_equal(output.y_observed, bundle.y_clean)


def test_non_label_corruptions_preserve_clean_and_observed_labels() -> None:
    registry = build_registry(__import__("pathlib").Path.cwd())
    bundle = synthetic_bundle()
    for family, corruption in registry.items():
        if family == "label_noise":
            continue
        output = corruption.apply(bundle, definition_for(family, corruption.target_space, corruption.config_hash, 0.8, 1001))
        if family == "distribution_shift":
            clean_by_row = dict(zip(bundle.row_ids.tolist(), bundle.y_clean.tolist()))
            expected_clean = np.array([clean_by_row[row_id] for row_id in output.row_ids.tolist()], dtype=bundle.y_clean.dtype)
            assert np.array_equal(output.y_clean, expected_clean), family
            assert np.array_equal(output.y_observed, expected_clean), family
            continue
        assert np.array_equal(output.y_clean, bundle.y_clean), family
        assert np.array_equal(output.y_observed, bundle.y_clean), family
