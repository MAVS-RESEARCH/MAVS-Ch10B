from __future__ import annotations

import argparse
from pathlib import Path

from mavs_ch10b.adapters.baseline_runner import run_clean_baseline
from mavs_ch10b.verification.import_audit import run_import_audit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mavs-ch10b")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_parser = subparsers.add_parser("import-foundation")
    import_parser.add_argument("--config", type=Path, default=Path("configs/ch10a_import/source.yaml"))

    baseline_parser = subparsers.add_parser("run-clean-baseline")
    baseline_parser.add_argument("--config", type=Path, default=Path("configs/ch10a_import/source.yaml"))
    baseline_parser.add_argument("--tolerance", type=float, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    if args.command == "import-foundation":
        from mavs_ch10b.verification.hash_utils import console

        # Phase 1 console.log: records CLI dispatch for the Chapter 10A foundation import.
        console.log("phase1.cli.import_foundation_dispatch", repo_root=str(repo_root), config=str(args.config))
        run_import_audit(repo_root=repo_root, config_path=args.config)
        return 0
    if args.command == "run-clean-baseline":
        from mavs_ch10b.verification.hash_utils import console

        # Phase 1 console.log: records CLI dispatch for the clean baseline replay.
        console.log("phase1.cli.clean_baseline_dispatch", repo_root=str(repo_root), config=str(args.config), tolerance=args.tolerance)
        run_clean_baseline(repo_root=repo_root, config_path=args.config, tolerance=args.tolerance)
        return 0
    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
