from __future__ import annotations

import csv
from pathlib import Path


def test_audit_and_locked_primary_seed_roles_are_independent() -> None:
    repo_root = Path.cwd()
    locked = _seeds(repo_root / "results" / "stress_runs" / "phase3_locked_full_v1_prediction_index.csv", "primary")
    audit = _seeds(repo_root / "results" / "stress_runs" / "phase3_audit_full_v1_prediction_index.csv", "audit")
    assert locked == {1001, 1002, 1003}
    assert audit == {2001, 2002, 2003}
    assert locked.isdisjoint(audit)


def test_shadow_seed_role_is_separate_from_primary_and_audit_roles() -> None:
    repo_root = Path.cwd()
    locked_shadow = _seeds(repo_root / "results" / "stress_runs" / "phase3_locked_full_v1_prediction_index.csv", "shadow")
    audit_shadow = _seeds(repo_root / "results" / "stress_runs" / "phase3_audit_full_v1_prediction_index.csv", "shadow")
    assert locked_shadow == {9001, 9002}
    assert audit_shadow == {9001, 9002}
    assert locked_shadow.isdisjoint({1001, 1002, 1003, 2001, 2002, 2003})


def _seeds(path: Path, seed_role: str) -> set[int]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {int(row["corruption_seed"]) for row in csv.DictReader(handle) if row["seed_role"] == seed_role}
