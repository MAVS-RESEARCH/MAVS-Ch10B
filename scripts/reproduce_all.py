from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from mavs_ch10b.verification.hash_utils import console
from mavs_ch10b.verification.import_audit import validate_no_training_command


@dataclass(frozen=True)
class ReproductionStep:
    step_id: str
    description: str
    command: tuple[str, ...]
    heavy: bool = False


def build_reproduction_plan(run_mode: str) -> list[ReproductionStep]:
    return [
        ReproductionStep("import_ch10a_foundation", "Import Chapter 10A foundation", ("scripts/import_ch10a_foundation.py",)),
        ReproductionStep("run_clean_baseline", "Run clean baseline replay", ("scripts/run_clean_baseline.py",)),
        ReproductionStep("build_corruption_grid", "Build corruption grid", ("scripts/build_corruption_grid.py",)),
        ReproductionStep("run_locked_corruption_benchmark", "Run locked corruption benchmark", ("scripts/run_locked_corruption_benchmark.py",), heavy=True),
        ReproductionStep("run_audit_corruption_benchmark", "Run audit corruption benchmark", ("scripts/run_audit_corruption_benchmark.py",), heavy=True),
        ReproductionStep("build_robustness_metrics", "Build robustness metrics", ("scripts/build_robustness_metrics.py",)),
        ReproductionStep("build_robustness_curves", "Build robustness curves", ("scripts/build_robustness_curves.py",)),
        ReproductionStep("build_corruption_atlas", "Build Corruption Atlas", ("scripts/build_corruption_atlas.py",)),
        ReproductionStep("build_failure_map", "Build Failure Map", ("scripts/build_failure_map.py",)),
        ReproductionStep("build_robustness_report", "Build Robustness Report", ("scripts/build_robustness_report.py",)),
        ReproductionStep("hash_artifacts", "Hash artifacts", ("scripts/hash_artifacts.py",)),
        ReproductionStep("verify_artifacts", "Verify artifacts", ("scripts/verify_artifacts.py", "--run-mode", run_mode)),
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Chapter 10B Phase 6 reproduction harness.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--run-mode", choices=("exploratory", "final"), default="final")
    parser.add_argument(
        "--execution-mode",
        choices=("verify-existing", "full"),
        default="verify-existing",
        help="verify-existing hashes and verifies a prepared checkout; full executes every build step.",
    )
    parser.add_argument("--plan-only", action="store_true", help="Print the reproduction plan without executing commands.")
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    plan = build_reproduction_plan(args.run_mode)
    validate_no_training_command(["reproduce_all.py", *[part for step in plan for part in step.command]])
    # Phase 6 console.log: records reproduction harness dispatch.
    console.log(
        "phase6.script.reproduce_dispatch",
        repo_root=str(repo_root),
        run_mode=args.run_mode,
        execution_mode=args.execution_mode,
        plan_only=args.plan_only,
        steps=len(plan),
    )
    if args.plan_only:
        print(json.dumps([step.__dict__ for step in plan], indent=2, default=list), flush=True)
        # Phase 6 console.log: records reproduction harness plan-only completion.
        console.log("phase6.script.reproduce_plan_complete", steps=len(plan))
        return 0
    for index, step in enumerate(plan, start=1):
        if args.execution_mode == "verify-existing" and step.step_id not in {"hash_artifacts", "verify_artifacts"}:
            # Phase 6 console.log: records prepared-checkout reproduction step validation without heavy execution.
            console.log(
                "phase6.script.reproduce_step_verified_existing",
                step_index=index,
                step_id=step.step_id,
                description=step.description,
                command=list(step.command),
            )
            continue
        # Phase 6 console.log: records reproduction step execution start.
        console.log(
            "phase6.script.reproduce_step_start",
            step_index=index,
            step_id=step.step_id,
            description=step.description,
            command=list(step.command),
        )
        completed = subprocess.run(
            [sys.executable, *step.command],
            cwd=repo_root,
            env=_subprocess_env(repo_root),
            check=False,
            text=True,
        )
        # Phase 6 console.log: records reproduction step execution completion.
        console.log("phase6.script.reproduce_step_complete", step_index=index, step_id=step.step_id, returncode=completed.returncode)
        if completed.returncode != 0:
            # Phase 6 console.log: records reproduction harness failure.
            console.log("phase6.script.reproduce_failed", failed_step=step.step_id, returncode=completed.returncode)
            return completed.returncode
    # Phase 6 console.log: records reproduction harness successful completion.
    console.log("phase6.script.reproduce_complete", run_mode=args.run_mode, execution_mode=args.execution_mode, steps=len(plan))
    return 0


def _subprocess_env(repo_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    src_path = str(repo_root / "src")
    current = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src_path if not current else src_path + os.pathsep + current
    return env


if __name__ == "__main__":
    raise SystemExit(main())
