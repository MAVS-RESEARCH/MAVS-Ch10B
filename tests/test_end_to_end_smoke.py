from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def test_phase6_reproduce_plan_contains_all_workplan_steps() -> None:
    repo_root = Path.cwd()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    result = subprocess.run(
        [sys.executable, "scripts/reproduce_all.py", "--run-mode", "final", "--plan-only"],
        cwd=repo_root,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    lines = result.stdout.splitlines()
    payload_start = next(index for index, line in enumerate(lines) if line.strip() == "[")
    payload_end = max(index for index, line in enumerate(lines) if line.strip() == "]")
    plan = json.loads("\n".join(lines[payload_start : payload_end + 1]))
    step_ids = [step["step_id"] for step in plan]
    assert step_ids == [
        "import_ch10a_foundation",
        "run_clean_baseline",
        "build_corruption_grid",
        "run_locked_corruption_benchmark",
        "run_audit_corruption_benchmark",
        "build_robustness_metrics",
        "build_robustness_curves",
        "build_corruption_atlas",
        "build_failure_map",
        "build_robustness_report",
        "hash_artifacts",
        "verify_artifacts",
    ]


def test_phase6_reproduce_final_verify_existing_succeeds() -> None:
    repo_root = Path.cwd()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    result = subprocess.run(
        [sys.executable, "scripts/reproduce_all.py", "--run-mode", "final"],
        cwd=repo_root,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
