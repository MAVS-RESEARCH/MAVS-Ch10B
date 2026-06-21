from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mavs_ch10b.reporting.failure_map import build_failure_map
from mavs_ch10b.reporting.tables import build_system_delta_table, load_metric_rows
from mavs_ch10b.verification.hash_utils import console
from mavs_ch10b.verification.import_audit import validate_no_training_command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Phase 5 Failure Map.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    validate_no_training_command([Path(sys.argv[0]).name, *sys.argv[1:]])
    repo_root = args.repo_root.resolve()
    # Phase 5 console.log: records Failure Map script dispatch.
    console.log("phase5.script.failure_map_dispatch", repo_root=str(repo_root))
    metric_rows = load_metric_rows(repo_root)
    path = build_failure_map(repo_root, metric_rows, build_system_delta_table(metric_rows))
    # Phase 5 console.log: records Failure Map script completion.
    console.log("phase5.script.failure_map_complete", path=str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
