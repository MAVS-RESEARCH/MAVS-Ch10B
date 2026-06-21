from __future__ import annotations

import numpy as np

from mavs_ch10b.corruptions.base import Corruption, CorruptionInput, CorruptionOutput, CorruptionRunDefinition, deterministic_rng


class MissingFeaturesCorruption(Corruption):
    def _apply(self, bundle: CorruptionInput, definition: CorruptionRunDefinition) -> CorruptionOutput:
        level = float(definition.level)
        features = np.array(bundle.features, dtype=np.float64, copy=True)
        mask = np.zeros_like(features, dtype=bool)
        if level > 0.0:
            rng = deterministic_rng(definition)
            fraction = min(1.0, float(self.parameters["max_missing_fraction"]) * level)
            mask = rng.random(features.shape) < fraction
            features[mask] = float(self.parameters.get("fill_value", 0.0))
        return self._base_output(
            bundle,
            definition,
            features=features,
            changed_mask=mask,
            metadata={"max_missing_fraction": self.parameters["max_missing_fraction"], "fill_value": self.parameters.get("fill_value", 0.0)},
        )

