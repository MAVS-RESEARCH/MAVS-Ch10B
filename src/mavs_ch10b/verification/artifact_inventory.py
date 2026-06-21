from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mavs_ch10b.verification.hash_utils import console, dependency_versions, git_commit, hash_file, write_json


CATEGORY_PATTERNS: dict[str, tuple[str, ...]] = {
    "documentation": ("README.md", "WorkPlan.md", "Path.md", "LICENSE", "pyproject.toml"),
    "configs": ("configs/**/*.yaml",),
    "source": ("src/**/*.py",),
    "tests": ("tests/**/*.py",),
    "scripts": ("scripts/**/*.py",),
    "import_manifests": ("results/baseline_import/*.json", "results/baseline_import/*.csv", "results/baseline_import/*.md"),
    "corruption_manifests": ("results/corruption_manifests/*.json", "results/corruption_manifests/*.csv"),
    "stress_run_manifests": (
        "results/stress_runs/*_run_manifest.json",
        "results/stress_runs/*_prediction_index.csv",
        "results/stress_runs/*_trace_index.csv",
        "results/stress_runs/*_aggregate_index.csv",
    ),
    "metric_tables": ("results/metrics/**/*.json", "results/metrics/**/*.csv"),
    "robustness_curves": ("results/robustness_curves/**/*.json", "results/robustness_curves/**/*.csv"),
    "figures": ("results/figures/**/*.png",),
    "reports": ("results/reports/*.json", "results/reports/*.csv", "results/reports/*.md"),
}

SELF_REFERENTIAL_REPORTS = {
    "results/reports/artifact_inventory.json",
    "results/reports/verification_report.md",
}


def build_artifact_inventory(repo_root: Path) -> dict[str, Any]:
    resolved_root = repo_root.resolve()
    artifacts: list[dict[str, Any]] = []
    seen: set[str] = set()
    # Phase 6 console.log: records artifact inventory category scan start.
    console.log("phase6.inventory.scan_start", repo_root=str(resolved_root), categories=len(CATEGORY_PATTERNS))
    for category, patterns in CATEGORY_PATTERNS.items():
        category_paths = _category_paths(resolved_root, patterns)
        # Phase 6 console.log: records one artifact inventory category scan.
        console.log("phase6.inventory.category_scanned", category=category, candidates=len(category_paths))
        for path in category_paths:
            relative_path = _relative(resolved_root, path)
            if relative_path in SELF_REFERENTIAL_REPORTS or relative_path in seen or path.name == ".gitkeep":
                continue
            artifacts.append(_artifact_record(resolved_root, path, category))
            seen.add(relative_path)
    category_counts = {category: 0 for category in CATEGORY_PATTERNS}
    for artifact in artifacts:
        category_counts[str(artifact["category"])] += 1
    inventory = {
        "schema_version": "1.0",
        "phase": "phase6",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(resolved_root),
        "dependency_versions": dependency_versions(),
        "category_counts": category_counts,
        "total_artifacts": len(artifacts),
        "total_bytes": sum(int(artifact["bytes"]) for artifact in artifacts),
        "self_referential_reports_excluded": sorted(SELF_REFERENTIAL_REPORTS),
        "artifacts": sorted(artifacts, key=lambda item: (str(item["category"]), str(item["path"]))),
    }
    # Phase 6 console.log: records artifact inventory construction completion.
    console.log(
        "phase6.inventory.built",
        total_artifacts=inventory["total_artifacts"],
        total_bytes=inventory["total_bytes"],
        category_counts=category_counts,
    )
    return inventory


def write_artifact_inventory(repo_root: Path, output_path: Path) -> dict[str, Any]:
    inventory = build_artifact_inventory(repo_root)
    write_json(output_path, inventory)
    inventory["artifact_inventory_path"] = str(output_path)
    inventory["artifact_inventory_sha256"] = hash_file(output_path)
    # Phase 6 console.log: records artifact inventory persistence.
    console.log(
        "phase6.inventory.written",
        path=str(output_path),
        sha256=inventory["artifact_inventory_sha256"],
        total_artifacts=inventory["total_artifacts"],
    )
    return inventory


def _category_paths(repo_root: Path, patterns: tuple[str, ...]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        paths.extend(path for path in repo_root.glob(pattern) if path.is_file())
    return sorted(set(paths))


def _artifact_record(repo_root: Path, path: Path, category: str) -> dict[str, Any]:
    stat = path.stat()
    return {
        "category": category,
        "path": _relative(repo_root, path),
        "sha256": hash_file(path),
        "bytes": stat.st_size,
        "modified_at_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
    }


def _relative(repo_root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(repo_root)).replace("\\", "/")
