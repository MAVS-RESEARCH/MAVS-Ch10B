from __future__ import annotations

import csv
from pathlib import Path

from mavs_ch10b.evaluation.robustness_area import AREA_METRICS, trapezoid_area


def test_trapezoid_area_matches_fixed_levels() -> None:
    assert trapezoid_area([0.0, 0.5, 1.0], [1.0, 0.5, 0.0]) == 0.5


def test_area_table_records_directionality() -> None:
    path = Path.cwd() / "results" / "robustness_curves" / "robustness_curve_area.csv"
    assert path.exists()
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows
    assert {row["metric"] for row in rows} == set(AREA_METRICS)
    assert all(row["directionality"] for row in rows)
