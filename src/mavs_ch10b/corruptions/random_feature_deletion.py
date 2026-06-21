from __future__ import annotations

import numpy as np

from mavs_ch10b.corruptions.base import Corruption, CorruptionInput, CorruptionOutput, CorruptionRunDefinition, deterministic_rng


class RandomFeatureDeletionCorruption(Corruption):
    def _apply(self, bundle: CorruptionInput, definition: CorruptionRunDefinition) -> CorruptionOutput:
        level = float(definition.level)
        features = np.array(bundle.features, dtype=np.float64, copy=True)
        mask = np.zeros_like(features, dtype=bool)
        deleted_columns: list[str] = []
        if level > 0.0:
            rng = deterministic_rng(definition)
            max_fraction = float(self.parameters["max_deletion_fraction"])
            columns = features.shape[1]
            count = min(columns, max(1, int(np.ceil(columns * max_fraction * level))))
            selected = np.sort(rng.choice(columns, size=count, replace=False))
            features[:, selected] = float(self.parameters.get("fill_value", 0.0))
            mask[:, selected] = True
            deleted_columns = [bundle.feature_names[index] for index in selected]
        return self._base_output(
            bundle,
            definition,
            features=features,
            changed_mask=mask,
            metadata={"deleted_columns": deleted_columns, "fill_value": self.parameters.get("fill_value", 0.0)},
        )

