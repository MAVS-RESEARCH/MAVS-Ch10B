from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from mavs_ch10b.verification.hash_utils import console
from mavs_ch10b.verification.release_gate import verify_phase6_release


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Phase 6 verification gate.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--run-mode", choices=("exploratory", "final"), default="final")
    parser.add_argument("--inventory", type=Path, default=Path("results/reports/artifact_inventory.json"))
    parser.add_argument("--report", type=Path, default=Path("results/reports/verification_report.md"))
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    inventory_path = args.inventory if args.inventory.is_absolute() else repo_root / args.inventory
    report_path = args.report if args.report.is_absolute() else repo_root / args.report
    # Phase 6 console.log: records verification script dispatch.
    console.log(
        "phase6.script.verify_dispatch",
        repo_root=str(repo_root),
        run_mode=args.run_mode,
        inventory=str(inventory_path),
        report=str(report_path),
    )
    report = verify_phase6_release(repo_root, inventory_path, report_path, args.run_mode)
    # Phase 6 console.log: records verification script completion.
    console.log("phase6.script.verify_complete", overall_status=report["overall_status"], report=str(report_path))
    return 0 if report["overall_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
