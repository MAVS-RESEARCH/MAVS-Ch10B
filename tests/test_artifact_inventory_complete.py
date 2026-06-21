from __future__ import annotations

import json
from pathlib import Path

from mavs_ch10b.verification.artifact_inventory import CATEGORY_PATTERNS
from mavs_ch10b.verification.hash_utils import hash_file


def test_phase6_artifact_inventory_has_every_required_category() -> None:
    repo_root = Path.cwd()
    inventory_path = repo_root / "results" / "reports" / "artifact_inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    counts = inventory["category_counts"]
    for category in CATEGORY_PATTERNS:
        assert counts[category] > 0, category
    assert inventory["total_artifacts"] == len(inventory["artifacts"])


def test_phase6_artifact_inventory_hashes_match_current_files() -> None:
    repo_root = Path.cwd()
    inventory = json.loads((repo_root / "results" / "reports" / "artifact_inventory.json").read_text(encoding="utf-8"))
    for artifact in inventory["artifacts"]:
        path = repo_root / artifact["path"]
        assert path.exists(), artifact["path"]
        assert artifact["sha256"] == hash_file(path), artifact["path"]
