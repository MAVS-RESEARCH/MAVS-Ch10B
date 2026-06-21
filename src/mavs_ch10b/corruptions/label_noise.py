from __future__ import annotations

import numpy as np

from mavs_ch10b.corruptions.base import Corruption, CorruptionInput, CorruptionOutput, CorruptionRunDefinition, deterministic_rng


class LabelNoiseCorruption(Corruption):
    def _apply(self, bundle: CorruptionInput, definition: CorruptionRunDefinition) -> CorruptionOutput:
        level = float(definition.level)
        y_observed = np.array(bundle.y_clean, dtype=np.int8, copy=True)
        mask = np.zeros_like(y_observed, dtype=bool)
        if level > 0.0:
            rng = deterministic_rng(definition)
            fraction = min(1.0, float(self.parameters["max_flip_fraction"]) * level)
            count = int(np.floor(len(y_observed) * fraction))
            if count > 0:
                selected = rng.choice(len(y_observed), size=count, replace=False)
                y_observed[selected] = 1 - y_observed[selected]
                mask[selected] = True
        return self._base_output(
            bundle,
            definition,
            y_observed=y_observed,
            changed_mask=mask,
            metadata={"max_flip_fraction": self.parameters["max_flip_fraction"], "flipped_labels": int(mask.sum())},
        )

