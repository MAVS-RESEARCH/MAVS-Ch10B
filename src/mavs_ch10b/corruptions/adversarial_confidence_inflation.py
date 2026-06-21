from __future__ import annotations

import numpy as np

from mavs_ch10b.corruptions.base import Corruption, CorruptionInput, CorruptionOutput, CorruptionRunDefinition, deterministic_rng, supports_from_probabilities


class AdversarialConfidenceInflationCorruption(Corruption):
    def _apply(self, bundle: CorruptionInput, definition: CorruptionRunDefinition) -> CorruptionOutput:
        level = float(definition.level)
        probabilities = np.array(bundle.probabilities, dtype=np.float64, copy=True)
        mask = np.zeros_like(probabilities, dtype=bool)
        if level > 0.0:
            rng = deterministic_rng(definition)
            strength = float(self.parameters["max_inflation_strength"]) * level
            eligible_fraction = min(1.0, float(self.parameters.get("max_eligible_fraction", 1.0)) * level)
            predictions = (probabilities >= 0.5).astype(np.int8)
            labels = bundle.y_clean.reshape(-1, 1)
            eligible = predictions != labels
            eligible_indices = np.argwhere(eligible)
            count = int(np.floor(len(eligible_indices) * eligible_fraction))
            if count > 0:
                chosen = eligible_indices[rng.choice(len(eligible_indices), size=count, replace=False)]
                for row_index, specialist_index in chosen:
                    if bundle.y_clean[row_index] == 0:
                        probabilities[row_index, specialist_index] = probabilities[row_index, specialist_index] + (1.0 - probabilities[row_index, specialist_index]) * strength
                    else:
                        probabilities[row_index, specialist_index] = probabilities[row_index, specialist_index] * (1.0 - strength)
                    mask[row_index, specialist_index] = True
            probabilities = np.clip(probabilities, 0.0, 1.0)
        return self._base_output(
            bundle,
            definition,
            probabilities=probabilities,
            supports=supports_from_probabilities(probabilities),
            changed_mask=mask,
            metadata={"label_aware": True, "max_inflation_strength": self.parameters["max_inflation_strength"], "modified_scores": int(mask.sum())},
        )

