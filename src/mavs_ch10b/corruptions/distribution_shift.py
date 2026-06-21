from __future__ import annotations

import numpy as np

from mavs_ch10b.corruptions.base import Corruption, CorruptionInput, CorruptionOutput, CorruptionRunDefinition


class DistributionShiftCorruption(Corruption):
    def _apply(self, bundle: CorruptionInput, definition: CorruptionRunDefinition) -> CorruptionOutput:
        level = float(definition.level)
        rows = bundle.features.shape[0]
        selected = np.arange(rows)
        descriptor = {"mode": self.parameters.get("score_mode", "feature_norm"), "retention_fraction": 1.0}
        if level > 0.0:
            min_retention = float(self.parameters["min_retention_fraction"])
            retention = 1.0 - (1.0 - min_retention) * level
            keep = max(1, int(np.ceil(rows * retention)))
            scores = np.linalg.norm(bundle.features, axis=1)
            tie_breaker = np.arange(rows) / max(rows, 1)
            order = np.lexsort((tie_breaker, -scores))
            selected = np.sort(order[:keep])
            descriptor = {
                "mode": self.parameters.get("score_mode", "feature_norm"),
                "retention_fraction": float(retention),
                "input_rows": int(rows),
                "output_rows": int(len(selected)),
            }
        mask = np.zeros(rows, dtype=bool)
        mask[selected] = True
        return self._base_output(
            bundle,
            definition,
            row_ids=np.array(bundle.row_ids[selected], copy=True),
            features=np.array(bundle.features[selected], copy=True),
            y_clean=np.array(bundle.y_clean[selected], copy=True),
            y_observed=np.array(bundle.y_clean[selected], copy=True),
            probabilities=np.array(bundle.probabilities[selected], copy=True),
            supports=np.array(bundle.supports[selected], copy=True),
            changed_mask=mask,
            distribution_shift_descriptor=descriptor,
            metadata={"selected_rows": int(len(selected))},
        )

