# MAVS Chapter 10B Robustness Benchmarks

This repository implements the MAVS Chapter 10B robustness benchmark program. Its purpose is to test whether the completed Chapter 10A systems fail more safely under adverse conditions.

## Phase 1 Scope

Phase 1 imports the frozen Chapter 10A benchmark foundation:

- trained specialists
- MAVS-GC implementation
- comparison baselines
- frozen system choices
- dataset, checkpoint, split, config, trace, and report manifests

No training is performed in Phase 1.

## Required Local Dependency

The Chapter 10A source repository alone is not sufficient because the large generated artifacts are intentionally not tracked by git. Phase 1 expects a local completed Chapter 10A artifact repository. The default configured path is:

```powershell
C:\Users\Saif malik\MAVS-Ch10A
```

Override it by editing `configs/ch10a_import/source.yaml` or by setting `MAVS_CH10A_ROOT`.

## Phase 1 Commands

```powershell
python scripts/import_ch10a_foundation.py
python scripts/run_clean_baseline.py
python -m pytest -q
```

Generated Phase 1 artifacts:

- `results/baseline_import/ch10a_import_manifest.json`
- `results/baseline_import/ch10a_import_report.md`
- `results/baseline_import/clean_replay_metrics.csv`
- `results/baseline_import/clean_replay_comparison.csv`
- `results/baseline_import/clean_replay_manifest.json`
- `results/baseline_import/clean_replay_compatibility_report.md`

## Documentation

- `WorkPlan.md` defines the phase-by-phase execution contract.
- `Path.md` records implementation details, commands, artifacts, stress-test evidence, deviations, and line references for Phase 1 `console.log(...)` instrumentation.

