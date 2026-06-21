from __future__ import annotations

import json
from pathlib import Path

from mavs_ch10b.verification.release_gate import audit_seed_overlap, final_run_mode_violations


def test_final_run_guard_rejects_exploratory_metadata_on_final_runs() -> None:
    manifests = [
        {"run_id": "phase6_final_locked_v1", "run_mode": "exploratory"},
        {"run_id": "phase6_final_audit_v1", "run_mode": "final"},
    ]
    assert final_run_mode_violations(manifests) == ["phase6_final_locked_v1:exploratory"]


def test_final_run_guard_accepts_current_nonfinal_exploratory_archives() -> None:
    manifests = [
        {"run_id": "phase3_locked_full_v1", "run_mode": "exploratory"},
        {"run_id": "phase3_audit_full_v1", "run_mode": "exploratory"},
    ]
    assert final_run_mode_violations(manifests) == []


def test_locked_and_audit_seed_guard_has_no_overlap() -> None:
    assert audit_seed_overlap(Path.cwd()) == []


def test_phase6_verification_report_overall_status_passes() -> None:
    report_text = (Path.cwd() / "results" / "reports" / "verification_report.md").read_text(encoding="utf-8")
    assert "Overall status: `pass`" in report_text
    assert "`anti_overfitting_final_run_guards` | `pass`" in report_text
