from __future__ import annotations

import numpy as np

from mavs_ch10b.evaluation.safety import conditional_unsafe_acceptance, unsafe_acceptance_rate


def test_unsafe_acceptance_uses_clean_negative_denominator() -> None:
    decisions = np.array([1, 1, 0, 1, 0], dtype=np.int8)
    y_clean = np.array([0, 0, 0, 1, 1], dtype=np.int8)
    assert unsafe_acceptance_rate(decisions, y_clean) == 2.0 / 3.0


def test_conditional_unsafe_acceptance_filters_condition() -> None:
    decisions = np.array([1, 1, 0, 1], dtype=np.int8)
    y_clean = np.array([0, 0, 0, 1], dtype=np.int8)
    condition = np.array([True, False, True, True])
    assert conditional_unsafe_acceptance(decisions, y_clean, condition) == 0.5
