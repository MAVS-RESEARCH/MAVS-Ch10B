from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mavs_ch10b.verification.hash_utils import console, dependency_versions, git_commit, hash_file, hash_json


def build_reproducibility_manifest(
    repo_root: Path,
    config_path: Path,
    output_paths: list[Path],
    claim_support: list[dict[str, Any]],
    row_counts: dict[str, int],
    run_modes: list[str],
) -> dict[str, Any]:
    inputs = _input_artifacts(repo_root, config_path)
    outputs = [{"path": _relative(repo_root, path), "sha256": hash_file(path), "role": _role_for(path)} for path in output_paths]
    manifest = {
        "schema_version": "1.0",
        "phase": "phase5",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(repo_root),
        "config_path": _relative(repo_root, config_path),
        "config_sha256": hash_file(config_path),
        "run_modes": run_modes,
        "dependency_versions": dependency_versions(),
        "row_counts": row_counts,
        "inputs": inputs,
        "outputs": outputs,
        "claim_support": claim_support,
        "anti_overfitting_controls": {
            "no_training_performed_in_phase5": True,
            "locked_and_audit_reported_separately": True,
            "corruption_seed_protocol_reported": True,
            "claims_require_artifact_support": True,
            "universal_superiority_claim_allowed": False,
        },
    }
    manifest["manifest_payload_sha256"] = hash_json(manifest)
    # Phase 5 console.log: records reproducibility manifest construction.
    console.log("phase5.repro_manifest.built", inputs=len(inputs), outputs=len(outputs), claims=len(claim_support))
    return manifest


def write_reproducibility_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # Phase 5 console.log: records reproducibility manifest persistence.
    console.log("phase5.repro_manifest.written", path=str(path), sha256=hash_file(path), claims=len(manifest["claim_support"]))


def validate_claim_support(repo_root: Path, claims: list[dict[str, Any]]) -> None:
    for claim in claims:
        if not claim.get("artifacts"):
            raise ValueError(f"Claim has no artifact support: {claim.get('id')}")
        for artifact in claim["artifacts"]:
            path = repo_root / artifact["path"]
            if not path.exists():
                raise FileNotFoundError(f"Claim artifact does not exist: {path}")
            actual = hash_file(path)
            if artifact.get("sha256") != actual:
                raise ValueError(f"Claim artifact hash mismatch for {path}")
    # Phase 5 console.log: records claim-to-artifact validation.
    console.log("phase5.repro_manifest.claim_support_validated", claims=len(claims))


def _input_artifacts(repo_root: Path, config_path: Path) -> list[dict[str, str]]:
    paths = [
        config_path,
        repo_root / "WorkPlan.md",
        repo_root / "results" / "baseline_import" / "ch10a_import_manifest.json",
        repo_root / "results" / "baseline_import" / "clean_replay_manifest.json",
        repo_root / "results" / "corruption_manifests" / "corruption_grid_manifest.json",
        repo_root / "results" / "stress_runs" / "phase3_locked_full_v1_run_manifest.json",
        repo_root / "results" / "stress_runs" / "phase3_audit_full_v1_run_manifest.json",
        repo_root / "results" / "metrics" / "locked_corruption" / "metric_manifest.json",
        repo_root / "results" / "metrics" / "audit_corruption" / "metric_manifest.json",
        repo_root / "results" / "robustness_curves" / "curve_manifest.json",
    ]
    records = [{"path": _relative(repo_root, path), "sha256": hash_file(path), "role": _role_for(path)} for path in paths]
    # Phase 5 console.log: records report input artifact manifest construction.
    console.log("phase5.repro_manifest.input_artifacts_built", inputs=len(records))
    return records


def _role_for(path: Path) -> str:
    name = path.name
    if name.endswith(".md"):
        return "report_or_documentation"
    if name.endswith(".csv"):
        return "table"
    if name.endswith(".png"):
        return "figure"
    if name.endswith(".json"):
        return "manifest"
    if name.endswith((".yaml", ".yml")):
        return "config"
    return "artifact"


def _relative(repo_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(repo_root)).replace("\\", "/")
    except ValueError:
        return str(path)
