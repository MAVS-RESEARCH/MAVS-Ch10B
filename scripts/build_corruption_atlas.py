from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mavs_ch10b.reporting.corruption_atlas import build_corruption_atlas
from mavs_ch10b.reporting.tables import load_area_rows, load_metric_rows
from mavs_ch10b.verification.hash_utils import console
from mavs_ch10b.verification.import_audit import validate_no_training_command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Phase 5 Corruption Atlas.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    validate_no_training_command([Path(sys.argv[0]).name, *sys.argv[1:]])
    repo_root = args.repo_root.resolve()
    # Phase 5 console.log: records Corruption Atlas script dispatch.
    console.log("phase5.script.corruption_atlas_dispatch", repo_root=str(repo_root))
    path = build_corruption_atlas(repo_root, load_metric_rows(repo_root), load_area_rows(repo_root))
    # Phase 5 console.log: records Corruption Atlas script completion.
    console.log("phase5.script.corruption_atlas_complete", path=str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
