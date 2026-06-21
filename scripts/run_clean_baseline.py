from __future__ import annotations

import argparse
from pathlib import Path

from mavs_ch10b.adapters.baseline_runner import run_clean_baseline
from mavs_ch10b.verification.hash_utils import console
from mavs_ch10b.verification.import_audit import validate_no_training_command


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="run-clean-baseline")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=Path("configs/ch10a_import/source.yaml"))
    parser.add_argument("--tolerance", type=float, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_no_training_command(["run_clean_baseline.py", *([] if argv is None else argv)])
    repo_root = args.repo_root.resolve()
    # Phase 1 console.log: records clean baseline script dispatch.
    console.log("phase1.script.clean_baseline_dispatch", repo_root=str(repo_root), config=str(args.config), tolerance=args.tolerance)
    manifest = run_clean_baseline(repo_root=repo_root, config_path=args.config, tolerance=args.tolerance)
    # Phase 1 console.log: records clean baseline script completion.
    console.log("phase1.script.clean_baseline_complete", comparison_failures=manifest["comparison_failures"], metric_rows=manifest["metric_rows"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

