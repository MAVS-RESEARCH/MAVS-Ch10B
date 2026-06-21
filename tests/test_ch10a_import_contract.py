from __future__ import annotations

from pathlib import Path

from mavs_ch10b.adapters.ch10a_artifacts import REQUIRED_DATASET_IDS, REQUIRED_SPECIALIST_IDS, REQUIRED_SYSTEM_IDS, validate_ch10a_foundation
from mavs_ch10b.adapters.ch10a_source import locate_ch10a_source


def test_ch10a_source_and_foundation_contract() -> None:
    repo_root = Path.cwd()
    source = locate_ch10a_source(repo_root)
    validation = validate_ch10a_foundation(source, verify_inventory=False, verify_trace_schema=False)
    assert validation.verification_report_status == "pass"
    assert set(validation.checkpoint_hashes) == set(REQUIRED_DATASET_IDS)
    assert all(set(values) == set(REQUIRED_SPECIALIST_IDS) for values in validation.checkpoint_hashes.values())
    assert set(REQUIRED_SYSTEM_IDS) == {
        "single_model",
        "mean_ensemble",
        "static_weighted_ensemble",
        "veto_mavs",
        "pure_mavs_gc",
    }

