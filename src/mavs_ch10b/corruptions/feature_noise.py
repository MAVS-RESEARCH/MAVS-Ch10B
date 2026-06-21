from __future__ import annotations

import numpy as np

from mavs_ch10b.corruptions.base import Corruption, CorruptionInput, CorruptionOutput, CorruptionRunDefinition, deterministic_rng


class FeatureNoiseCorruption(Corruption):
    def _apply(self, bundle: CorruptionInput, definition: CorruptionRunDefinition) -> CorruptionOutput:
        level = float(definition.level)
        features = np.array(bundle.features, dtype=np.float64, copy=True)
        mask = np.zeros_like(features, dtype=bool)
        if level > 0.0:
            rng = deterministic_rng(definition)
            scale = np.nanstd(bundle.features, axis=0)
            scale = np.where(np.isfinite(scale) & (scale > 0.0), scale, 1.0)
            noise = rng.normal(loc=0.0, scale=scale * float(self.parameters["max_std_multiplier"]) * level, size=features.shape)
            features = features + noise
            clip_value = float(self.parameters.get("finite_clip", 1000000.0))
            features = np.clip(features, -clip_value, clip_value)
            mask = np.abs(noise) > 0.0
        return self._base_output(
            bundle,
            definition,
            features=features,
            changed_mask=mask,
            metadata={"mode": self.parameters.get("mode", "additive_gaussian"), "max_std_multiplier": self.parameters["max_std_multiplier"]},
        )

