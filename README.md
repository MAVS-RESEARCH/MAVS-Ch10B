# MAVS Chapter 10B Robustness Benchmarks

This repository contains the MAVS Chapter 10B robustness benchmark artifact. It evaluates whether the completed Chapter 10A MAVS systems and comparison baselines fail more safely under controlled corruptions, stress conditions, and governance trace analysis.

The repository is organized around the phase contract in `WorkPlan.md`. The implementation trail, command evidence, artifact hashes, deviations, and console log line references are recorded in `Path.md`.

## Current Status

Phase 6 is implemented and pushed.

- Verification report: `results/reports/verification_report.md`
- Artifact inventory: `results/reports/artifact_inventory.json`
- Verification status: `pass`
- Artifact inventory count: `520`
- Test suite status at Phase 6 completion: `49 passed`

Important qualification: the archived full Phase 3 stress runs are marked `exploratory`. Phase 6 verifies prepared-checkout artifact integrity and arms final-run guards. It does not relabel exploratory evidence as final release stress evidence.

## Required Local Dependency

Chapter 10B imports the completed Chapter 10A artifact repository. The Chapter 10A source repository alone is not sufficient because large generated artifacts are intentionally not tracked by git.

Default local path:

```powershell
C:\Users\Saif malik\MAVS-Ch10A
```

Override the path by editing `configs/ch10a_import/source.yaml` or by setting `MAVS_CH10A_ROOT`.

## Reproduction And Verification

Prepared-checkout verification:

```powershell
python scripts/reproduce_all.py --run-mode final
```

This command validates the complete reproduction plan, hashes the current artifacts, and runs the Phase 6 verification gate. In prepared-checkout mode it does not rerun the heavy full stress matrices.

Full rebuild mode:

```powershell
python scripts/reproduce_all.py --run-mode final --execution-mode full
```

Use full rebuild mode only when the Chapter 10A local artifacts are available and the operator intends to rerun the complete Chapter 10B pipeline.

Run the test suite:

```powershell
pytest
```

## Phase Outputs

Phase 1 imports and validates the Chapter 10A foundation:

- `results/baseline_import/ch10a_import_manifest.json`
- `results/baseline_import/ch10a_import_report.md`
- `results/baseline_import/clean_replay_manifest.json`
- `results/baseline_import/clean_replay_metrics.csv`
- `results/baseline_import/clean_replay_comparison.csv`

Phase 2 builds the corruption grid:

- `results/corruption_manifests/corruption_grid_manifest.json`
- `results/corruption_manifests/corruption_manifest_index.json`
- `results/corruption_manifests/corruption_manifest_index.csv`

Phase 3 stores locked and audit stress run indexes:

- `results/stress_runs/phase3_locked_full_v1_run_manifest.json`
- `results/stress_runs/phase3_audit_full_v1_run_manifest.json`
- `results/stress_runs/*_prediction_index.csv`
- `results/stress_runs/*_trace_index.csv`
- `results/stress_runs/*_aggregate_index.csv`

Phase 4 builds robustness metrics and curves:

- `results/metrics/locked_corruption/metric_manifest.json`
- `results/metrics/audit_corruption/metric_manifest.json`
- `results/robustness_curves/curve_manifest.json`
- `results/robustness_curves/robustness_curve_area.csv`
- `results/figures/robustness_curves/*.png`

Phase 5 builds analysis reports and figures:

- `results/reports/robustness_report.md`
- `results/reports/corruption_atlas.md`
- `results/reports/failure_map.md`
- `results/reports/robustness_tables.csv`
- `results/reports/robustness_system_deltas.csv`
- `results/reports/robustness_reproducibility_manifest.json`
- `results/figures/governance_severity_distribution.png`
- `results/figures/threshold_distribution.png`
- `results/figures/unsafe_acceptance_by_corruption.png`
- `results/figures/robustness_area_by_system.png`

Phase 6 verifies release readiness:

- `scripts/reproduce_all.py`
- `scripts/hash_artifacts.py`
- `scripts/verify_artifacts.py`
- `results/reports/artifact_inventory.json`
- `results/reports/verification_report.md`
- `tests/test_end_to_end_smoke.py`
- `tests/test_artifact_inventory_complete.py`
- `tests/test_final_run_guards.py`

## No-Retraining Policy

Chapter 10B does not train models. It imports frozen Chapter 10A specialists and systems, then evaluates them under corruption. Phase 6 checks that no model-training artifacts are created by Chapter 10B final commands and that forbidden training commands are absent from recorded manifests.

## Documentation

- `WorkPlan.md` defines the phase-by-phase execution contract.
- `Path.md` records what was implemented, whether each phase followed `WorkPlan.md`, command outputs, artifact hashes, stress-test evidence, deviations, and console log instrumentation references.
