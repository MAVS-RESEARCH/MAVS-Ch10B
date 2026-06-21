from __future__ import annotations

import numpy as np

from mavs_ch10b.corruptions.base import Corruption, CorruptionInput, CorruptionOutput, CorruptionRunDefinition, supports_from_probabilities


class ConfidenceDistortionCorruption(Corruption):
    def _apply(self, bundle: CorruptionInput, definition: CorruptionRunDefinition) -> CorruptionOutput:
        level = float(definition.level)
        epsilon = float(self.parameters.get("epsilon", 1.0e-6))
        probabilities = np.array(bundle.probabilities, dtype=np.float64, copy=True)
        mask = np.zeros_like(probabilities, dtype=bool)
        if level > 0.0:
            max_temperature = float(self.parameters["max_temperature"])
            temperature = 1.0 + (max_temperature - 1.0) * level
            clipped = np.clip(probabilities, epsilon, 1.0 - epsilon)
            logits = np.log(clipped / (1.0 - clipped))
            probabilities = 1.0 / (1.0 + np.exp(-(logits / temperature)))
            probabilities = np.clip(probabilities, 0.0, 1.0)
            mask = np.abs(probabilities - bundle.probabilities) > 0.0
        return self._base_output(
            bundle,
            definition,
            probabilities=probabilities,
            supports=supports_from_probabilities(probabilities),
            changed_mask=mask,
            metadata={"mode": "temperature_compression", "max_temperature": self.parameters["max_temperature"]},
        )

