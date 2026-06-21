from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from mavs_ch10b.verification.artifact_inventory import write_artifact_inventory
from mavs_ch10b.verification.hash_utils import console


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Phase 6 artifact inventory.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("results/reports/artifact_inventory.json"))
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    output_path = args.output if args.output.is_absolute() else repo_root / args.output
    # Phase 6 console.log: records artifact hashing script dispatch.
    console.log("phase6.script.hash_dispatch", repo_root=str(repo_root), output=str(output_path))
    inventory = write_artifact_inventory(repo_root, output_path)
    # Phase 6 console.log: records artifact hashing script completion.
    console.log(
        "phase6.script.hash_complete",
        output=str(output_path),
        sha256=inventory["artifact_inventory_sha256"],
        total_artifacts=inventory["total_artifacts"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
