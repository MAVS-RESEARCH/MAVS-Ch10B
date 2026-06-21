from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from mavs_ch10b.verification.hash_utils import console


@dataclass(frozen=True)
class Chapter10ASource:
    repo_root: Path
    source_repo_url: str
    config: dict[str, Any]

    @property
    def src_path(self) -> Path:
        return self.repo_root / "src"


def load_source_config(repo_root: Path, config_path: Path) -> dict[str, Any]:
    resolved = config_path if config_path.is_absolute() else repo_root / config_path
    if not resolved.exists():
        raise FileNotFoundError(f"Missing Chapter 10A source config: {resolved}")
    config = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    # Phase 1 console.log: records Chapter 10A source configuration loading.
    console.log("phase1.ch10a_source.config_loaded", path=str(resolved), keys=sorted(config.keys()))
    return config


def locate_ch10a_source(repo_root: Path, config_path: Path = Path("configs/ch10a_import/source.yaml")) -> Chapter10ASource:
    config = load_source_config(repo_root, config_path)
    candidates = _candidate_paths(repo_root, config)
    # Phase 1 console.log: records Chapter 10A source candidate enumeration.
    console.log("phase1.ch10a_source.candidates_built", candidates=[str(path) for path in candidates])
    for candidate in candidates:
        if _is_valid_ch10a_root(candidate):
            source = Chapter10ASource(
                repo_root=candidate.resolve(),
                source_repo_url=str(config.get("source_repo_url", "")),
                config=config,
            )
            # Phase 1 console.log: records selected Chapter 10A artifact repository.
            console.log("phase1.ch10a_source.located", repo_root=str(source.repo_root), source_repo_url=source.source_repo_url)
            return source
    raise FileNotFoundError(f"No valid Chapter 10A artifact repository found from candidates: {[str(path) for path in candidates]}")


def ensure_ch10a_importable(source: Chapter10ASource) -> None:
    src_path = str(source.src_path)
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    # Phase 1 console.log: records Chapter 10A source import path registration.
    console.log("phase1.ch10a_source.import_path_ready", src_path=src_path, present=src_path in sys.path)


def _candidate_paths(repo_root: Path, config: dict[str, Any]) -> list[Path]:
    raw_candidates: list[str] = []
    env_value = os.environ.get("MAVS_CH10A_ROOT")
    if env_value:
        raw_candidates.append(env_value)
    local_artifact_path = config.get("local_artifact_path")
    if local_artifact_path:
        raw_candidates.append(str(local_artifact_path))
    raw_candidates.extend(str(item) for item in config.get("fallback_candidates", []))
    raw_candidates.append(str(repo_root.parent / "MAVS-Ch10A"))
    seen: set[str] = set()
    resolved: list[Path] = []
    for raw in raw_candidates:
        path = Path(os.path.expandvars(raw)).expanduser()
        if not path.is_absolute():
            path = (repo_root / path).resolve()
        key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        resolved.append(path)
    return resolved


def _is_valid_ch10a_root(path: Path) -> bool:
    return (
        path.exists()
        and (path / "pyproject.toml").exists()
        and (path / "src" / "mavs_ch10a" / "__init__.py").exists()
        and (path / "results" / "reports" / "reproducibility_manifest.json").exists()
    )

