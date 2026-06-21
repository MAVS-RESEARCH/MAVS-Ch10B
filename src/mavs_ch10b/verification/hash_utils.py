from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ResearchConsole:
    enabled: bool = True

    def log(self, event: str, **fields: Any) -> None:
        if not self.enabled:
            return
        payload = {
            "event": event,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            **fields,
        }
        print(json.dumps(payload, sort_keys=True, default=str), flush=True)


console = ResearchConsole()


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_json(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # Phase 1 console.log: records JSON artifact persistence.
    console.log("phase1.hash_utils.json_written", path=str(path), sha256=hash_file(path))


def git_commit(repo_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def dependency_versions() -> dict[str, str]:
    versions: dict[str, str] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
    }
    for module_name in ("numpy", "pandas", "sklearn", "yaml", "joblib"):
        try:
            module = __import__(module_name)
            versions[module_name] = str(getattr(module, "__version__", "unknown"))
        except Exception:
            versions[module_name] = "unavailable"
    return versions

