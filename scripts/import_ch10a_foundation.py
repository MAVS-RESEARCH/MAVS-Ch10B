from __future__ import annotations

import argparse
from pathlib import Path

from mavs_ch10b.verification.hash_utils import console
from mavs_ch10b.verification.import_audit import run_import_audit, validate_no_training_command


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="import-ch10a-foundation")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=Path("configs/ch10a_import/source.yaml"))
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_no_training_command(["import_ch10a_foundation.py", *([] if argv is None else argv)])
    repo_root = args.repo_root.resolve()
    # Phase 1 console.log: records import script dispatch.
    console.log("phase1.script.import_dispatch", repo_root=str(repo_root), config=str(args.config))
    manifest = run_import_audit(repo_root=repo_root, config_path=args.config)
    # Phase 1 console.log: records import script completion.
    console.log("phase1.script.import_complete", manifest_path=manifest["report_path"], status=manifest["verification_report_status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

