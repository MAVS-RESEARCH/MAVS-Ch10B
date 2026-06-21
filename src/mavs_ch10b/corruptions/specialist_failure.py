from __future__ import annotations

import numpy as np

from mavs_ch10b.corruptions.base import Corruption, CorruptionInput, CorruptionOutput, CorruptionRunDefinition, supports_from_probabilities


class SpecialistFailureCorruption(Corruption):
    def _apply(self, bundle: CorruptionInput, definition: CorruptionRunDefinition) -> CorruptionOutput:
        level = float(definition.level)
        probabilities = np.array(bundle.probabilities, dtype=np.float64, copy=True)
        mask = np.zeros_like(probabilities, dtype=bool)
        failed_specialists: tuple[str, ...] = ()
        if level > 0.0:
            specialists = len(bundle.specialist_ids)
            failed_count = min(specialists, max(1, int(np.ceil(specialists * level))))
            failed_indices = np.arange(failed_count)
            failure_mode = str(self.parameters.get("failure_mode", "constant_uncertainty"))
            if failure_mode != "constant_uncertainty":
                raise ValueError(f"Unsupported specialist failure mode: {failure_mode}")
            probabilities[:, failed_indices] = float(self.parameters.get("uncertainty_probability", 0.5))
            mask[:, failed_indices] = True
            failed_specialists = tuple(bundle.specialist_ids[index] for index in failed_indices)
        return self._base_output(
            bundle,
            definition,
            probabilities=probabilities,
            supports=supports_from_probabilities(probabilities),
            changed_mask=mask,
            failed_specialists=failed_specialists,
            metadata={"failure_mode": self.parameters.get("failure_mode", "constant_uncertainty")},
        )

