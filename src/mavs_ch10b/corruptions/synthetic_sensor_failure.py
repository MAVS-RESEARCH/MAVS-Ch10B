from __future__ import annotations

import numpy as np

from mavs_ch10b.corruptions.base import Corruption, CorruptionInput, CorruptionOutput, CorruptionRunDefinition


class SyntheticSensorFailureCorruption(Corruption):
    def _apply(self, bundle: CorruptionInput, definition: CorruptionRunDefinition) -> CorruptionOutput:
        level = float(definition.level)
        features = np.array(bundle.features, dtype=np.float64, copy=True)
        mask = np.zeros_like(features, dtype=bool)
        affected_features: list[str] = []
        if level > 0.0:
            groups = build_feature_groups(features.shape[1], int(self.parameters["max_groups"]))
            group_count = min(len(groups), max(1, int(np.ceil(len(groups) * level))))
            selected_groups = groups[:group_count]
            selected_columns = np.array([col for group in selected_groups for col in group], dtype=int)
            features[:, selected_columns] = float(self.parameters.get("fill_value", 0.0))
            mask[:, selected_columns] = True
            affected_features = [bundle.feature_names[index] for index in selected_columns]
        return self._base_output(
            bundle,
            definition,
            features=features,
            changed_mask=mask,
            metadata={"affected_features": affected_features, "max_groups": self.parameters["max_groups"], "fill_value": self.parameters.get("fill_value", 0.0)},
        )


def build_feature_groups(columns: int, max_groups: int) -> list[list[int]]:
    group_count = max(1, min(columns, max_groups))
    indices = np.arange(columns)
    return [list(group.astype(int)) for group in np.array_split(indices, group_count)]

