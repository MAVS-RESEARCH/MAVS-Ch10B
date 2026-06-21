from __future__ import annotations

import hashlib
import json
from pathlib import Path


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_report_claims_reference_existing_hashed_artifacts() -> None:
    repo_root = Path.cwd()
    manifest_path = repo_root / "results" / "reports" / "robustness_reproducibility_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report_text = (repo_root / "results" / "reports" / "robustness_report.md").read_text(encoding="utf-8")
    claims = manifest["claim_support"]
    assert len(claims) >= 8
    for claim in claims:
        assert claim["id"] in report_text
        assert claim["artifacts"], claim["id"]
        for artifact in claim["artifacts"]:
            path = repo_root / artifact["path"]
            assert path.exists(), path
            assert artifact["sha256"] == _hash_file(path)


def test_manifest_outputs_reference_existing_artifacts() -> None:
    repo_root = Path.cwd()
    manifest = json.loads((repo_root / "results" / "reports" / "robustness_reproducibility_manifest.json").read_text(encoding="utf-8"))
    for artifact in manifest["inputs"] + manifest["outputs"]:
        path = repo_root / artifact["path"]
        assert path.exists(), path
        assert artifact["sha256"] == _hash_file(path)
    assert manifest["anti_overfitting_controls"]["no_training_performed_in_phase5"] is True
    assert manifest["anti_overfitting_controls"]["universal_superiority_claim_allowed"] is False
