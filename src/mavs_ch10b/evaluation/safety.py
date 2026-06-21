from __future__ import annotations

import numpy as np

from mavs_ch10b.evaluation.metrics import safe_divide


def unsafe_acceptance_rate(decisions: np.ndarray, y_clean: np.ndarray) -> float:
    negatives = int(np.sum(y_clean == 0))
    unsafe = int(np.sum((decisions == 1) & (y_clean == 0)))
    return safe_divide(unsafe, negatives)


def conditional_unsafe_acceptance(decisions: np.ndarray, y_clean: np.ndarray, condition: np.ndarray) -> float:
    mask = (y_clean == 0) & condition.astype(bool)
    unsafe = int(np.sum((decisions == 1) & mask))
    return safe_divide(unsafe, int(np.sum(mask)))
