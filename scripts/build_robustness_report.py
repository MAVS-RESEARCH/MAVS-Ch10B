from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mavs_ch10b.reporting.robustness_report import build_robustness_report
from mavs_ch10b.verification.hash_utils import console
from mavs_ch10b.verification.import_audit import validate_no_training_command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Phase 5 robustness report artifacts.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=Path("configs/reports/robustness_report.yaml"))
    args = parser.parse_args(argv)
    validate_no_training_command([Path(sys.argv[0]).name, *sys.argv[1:]])
    repo_root = args.repo_root.resolve()
    config_path = args.config if args.config.is_absolute() else repo_root / args.config
    # Phase 5 console.log: records Robustness Report script dispatch.
    console.log("phase5.script.robustness_report_dispatch", repo_root=str(repo_root), config=str(config_path))
    result = build_robustness_report(repo_root, config_path)
    # Phase 5 console.log: records Robustness Report script completion.
    console.log("phase5.script.robustness_report_complete", report_path=str(result["report_path"]), manifest_path=str(result["manifest_path"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
