from __future__ import annotations

import argparse
from pathlib import Path

from mavs_ch10b.corruptions.grid import build_corruption_grid, write_grid_manifest
from mavs_ch10b.verification.hash_utils import console


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="build-corruption-grid")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=Path("configs/corruptions/corruption_grid.yaml"))
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    # Phase 2 console.log: records corruption grid script dispatch.
    console.log("phase2.script.build_corruption_grid_dispatch", repo_root=str(repo_root), config=str(args.config))
    definitions = build_corruption_grid(repo_root, args.config)
    manifest = write_grid_manifest(repo_root, definitions, args.config)
    # Phase 2 console.log: records corruption grid script completion.
    console.log("phase2.script.build_corruption_grid_complete", definitions=len(definitions), manifest_path=manifest["manifest_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

