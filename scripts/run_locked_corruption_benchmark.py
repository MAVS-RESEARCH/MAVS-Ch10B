from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mavs_ch10b.stress.run_matrix import run_stress_matrix
from mavs_ch10b.verification.hash_utils import console


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Phase 3 locked corruption benchmark.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=Path("configs/experiments/locked_corruption_benchmark.yaml"))
    parser.add_argument("--run-id", type=str, default=None)
    parser.add_argument("--max-definitions", type=int, default=None)
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    # Phase 3 console.log: records locked corruption benchmark script dispatch.
    console.log("phase3.script.locked_dispatch", repo_root=str(repo_root), config=str(args.config), run_id=args.run_id)
    manifest = run_stress_matrix(
        repo_root=repo_root,
        config_path=args.config,
        run_id=args.run_id,
        max_definitions=args.max_definitions,
        command_line=[Path(sys.argv[0]).name, *sys.argv[1:]],
    )
    # Phase 3 console.log: records locked corruption benchmark script completion.
    console.log("phase3.script.locked_complete", run_id=manifest["run_id"], system_runs=manifest["system_run_count"], manifest_path=manifest["manifest_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
