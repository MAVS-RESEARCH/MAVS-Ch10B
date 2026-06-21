from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from mavs_ch10b.evaluation.aggregation import build_governance_delta_table
from mavs_ch10b.evaluation.curve_builder import build_curve_rows, write_curve_artifacts
from mavs_ch10b.evaluation.metrics import write_csv
from mavs_ch10b.evaluation.statistics import build_seed_level_bootstrap_cis, build_seed_level_variance
from mavs_ch10b.verification.hash_utils import console, hash_file, hash_json
from mavs_ch10b.verification.import_audit import validate_no_training_command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Phase 4 robustness curves from metric rows.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--bootstrap-iterations", type=int, default=500)
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    validate_no_training_command([Path(sys.argv[0]).name, *sys.argv[1:]])
    # Phase 4 console.log: records robustness curve script dispatch.
    console.log("phase4.script.curves_dispatch", repo_root=str(repo_root), bootstrap_iterations=args.bootstrap_iterations)
    metric_rows = load_all_metric_rows(repo_root)
    curve_rows = build_curve_rows(metric_rows)
    curve_info = write_curve_artifacts(
        curve_rows,
        repo_root / "results" / "robustness_curves",
        repo_root / "results" / "figures" / "robustness_curves",
    )
    for split_label in ("locked", "audit"):
        split_rows = [row for row in metric_rows if row["split_label"] == split_label]
        output_dir = repo_root / "results" / "metrics" / f"{split_label}_corruption"
        write_csv(output_dir / "governance_delta_table.csv", build_governance_delta_table(split_rows))
        write_csv(output_dir / "paired_bootstrap_cis.csv", build_seed_level_bootstrap_cis(split_rows, iterations=args.bootstrap_iterations))
        write_csv(output_dir / "seed_level_variance.csv", build_seed_level_variance(split_rows))
    manifest = {
        "schema_version": "1.0",
        "phase": "phase4",
        "metric_rows_loaded": len(metric_rows),
        "curve_rows": len(curve_rows),
        **curve_info,
        "bootstrap_iterations": args.bootstrap_iterations,
        "command_line": [Path(sys.argv[0]).name, *sys.argv[1:]],
    }
    manifest["manifest_payload_sha256"] = hash_json(manifest)
    manifest_path = repo_root / "results" / "robustness_curves" / "curve_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest["manifest_path"] = str(manifest_path)
    manifest["manifest_file_sha256"] = hash_file(manifest_path)
    # Phase 4 console.log: records robustness curve script completion.
    console.log("phase4.script.curves_complete", manifest_path=str(manifest_path), curve_rows=len(curve_rows), area_rows=curve_info["area_rows"])
    return 0


def load_all_metric_rows(repo_root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for split_label in ("locked", "audit"):
        path = repo_root / "results" / "metrics" / f"{split_label}_corruption" / "metric_rows.csv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows.extend(csv.DictReader(handle))
    # Phase 4 console.log: records metric row loading for robustness curve construction.
    console.log("phase4.script.metric_rows_loaded", rows=len(rows))
    return rows


if __name__ == "__main__":
    raise SystemExit(main())
