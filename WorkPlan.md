# MAVS Chapter 10B WorkPlan

## Source Authority

This workplan is grounded in the four source documents supplied by the user:

1. `MAVS Chapter 10B.pdf`
   - Controlling document for this repository.
   - Defines Chapter 10B as the robustness benchmark program.
   - Requires importing trained specialists, MAVS-GC, and baselines from Chapter 10A with no retraining.
   - Requires a parameterized corruption engine, governance stress testing, robustness evaluation, and final analysis artifacts.
2. `Mavs.pdf`
   - Defines MAVS as a governance-first AI architecture.
   - Requires all specialists to evaluate every input.
   - Requires governed consensus, diagnostics, severity, weights, optional mitigation, thresholds, hard veto behavior, and deterministic explanation traces.
3. `Mavs Research Bible - Chapter 10.pdf`
   - Defines Chapter 10 as the real benchmark program for MAVS.
   - Adds the global evidence standard: reproducible, statistically supported, observed across multiple datasets, observed against multiple baselines, and documented through traces and reports.
   - Defines Chapter 10B as the robustness program and expands the required corruption families and metrics.
4. `MAVS Research Bible - Chapter 10A Completion Report.pdf`
   - Confirms Chapter 10A is complete.
   - Confirms the Chapter 10A evidence was negative-to-mixed for universal predictive correctness.
   - Narrows the Chapter 10B purpose toward risk reduction, error shaping, safety controls, calibration behavior, distribution shift, adversarial resistance, and robustness under stress.

The Chapter 10B document controls the mission. When supporting documents add stricter or more complete requirements, this plan includes them unless they would move Chapter 10B into Chapter 10C reproducibility or later research chapters.

## Mission

Chapter 10B answers one research question:

**Does MAVS-GC fail more safely under adverse conditions?**

The repository exists to determine whether governance improves reliability when the world becomes imperfect. The objective is not to retrain better models, tune for state-of-the-art scores, or reinterpret the Chapter 10A accuracy result. The objective is to test the already completed Chapter 10A systems under systematic corruption and determine whether governance produces safer degradation than aggregation-only systems.

## Scope Boundary

In scope:

- Importing the completed Chapter 10A trained specialists, baselines, MAVS-GC implementation, frozen configs, splits, and artifact manifests.
- No retraining for the normal Chapter 10B program.
- The Chapter 10A datasets:
  - Breast Cancer Wisconsin
  - Adult Income
  - Credit Card Fraud
  - Bank Marketing
- The Chapter 10A specialist families:
  - Random Forest
  - Gradient Boosted Trees
  - MLP
- The shared Chapter 10 comparison systems:
  - Single Best Model
  - Mean Ensemble
  - Static Weighted Ensemble
  - Veto MAVS
  - Pure MAVS-GC
- Required corruption families:
  - Feature Noise
  - Missing Features
  - Random Feature Deletion
  - Label Noise
  - Confidence Distortion
  - Adversarial Confidence Inflation
  - Distribution Shift
  - Synthetic Sensor Failure
  - Specialist Failure
- Required metrics:
  - Accuracy Under Corruption
  - F1 Under Corruption
  - Unsafe Acceptance Rate
  - Failure Rate
  - Rejection Rate
  - Robustness Curve Area
  - Governance Severity
  - Governance Severity Distribution
  - Governance Threshold Distribution
- Required outputs:
  - Corruption traces
  - `robustness_curves/`
  - Robustness benchmark suite
  - Robustness Report
  - Corruption Atlas
  - Failure Map

Out of scope:

- New model training for performance improvement.
- Tuning model hyperparameters, ensemble weights, governance thresholds, or corruption grids on Chapter 10B results.
- Chapter 10C multi-seed reproducibility claims, except where independent stress seeds are needed to prevent overfitting.
- General intelligence, universal superiority, cross-domain validity, governance learning, self-governance, or scientific discovery claims.

## No-Retraining Policy

Chapter 10B must begin with the completed Chapter 10A artifacts. The normal execution path performs no model training. It imports frozen specialists and systems, then evaluates them under corruption.

If Chapter 10A generated artifacts are unavailable, Phase 1 must stop and record the blocker in `Path.md`. A reproduction-only retraining pass may be done only to reconstruct the exact Chapter 10A frozen artifacts from Chapter 10A configs and splits. Such a pass is not Chapter 10B training and must obey all Chapter 10A isolation rules:

- Train specialists only on the Chapter 10A train split.
- Select model and ensemble settings only from the allowed Chapter 10A validation/calibration data.
- Calibrate only on the Chapter 10A calibration split.
- Evaluate only on locked benchmark and audit benchmark splits.
- Freeze the reconstructed artifacts before any corruption result is inspected.
- Record every checkpoint hash, split hash, config hash, dependency version, and command in `Path.md`.

Any retrained or reconstructed artifact must then be brutally tested on benchmark data entirely separate from training data:

- Clean locked benchmark.
- Clean audit benchmark.
- Locked corruption benchmark with frozen corruption seeds.
- Audit corruption benchmark with independent corruption seeds.
- Optional shadow stress benchmark seeds used only for verification, never for tuning.

No claim may use training, validation, or calibration metrics as final robustness evidence.

## Repository Contract

This repository will be a reproducible Python benchmark package. The expected implementation style is to reuse Chapter 10A source interfaces where possible, add Chapter 10B adapters around them, and keep robustness code separate from the Chapter 10A accuracy code.

Planned top-level structure:

```text
configs/
  ch10a_import/
  corruptions/
  experiments/
  reports/
external/
  ch10a/
src/
  mavs_ch10b/
    adapters/
    corruptions/
    stress/
    evaluation/
    reporting/
    verification/
    cli.py
tests/
results/
  baseline_import/
  corruption_manifests/
  corruption_traces/
  stress_runs/
  metrics/
  robustness_curves/
  figures/
  reports/
scripts/
WorkPlan.md
Path.md
```

Generated datasets, checkpoints, full traces, predictions, and heavy stress outputs should be ignored by git unless a later publication decision explicitly tracks them. Final reports, tables, figures, manifests, artifact inventories, and verification reports should be tracked when small enough.

## Phase 1 - Baseline Import and Frozen Foundation

### Scope

Import the completed Chapter 10A systems and establish a stable robustness foundation.

This phase implements the Chapter 10B requirement:

- Import trained specialists.
- Import MAVS-GC.
- Import baselines.
- Do not retrain.
- Produce a stable benchmark foundation.

The imported foundation must include the Chapter 10A trained specialist checkpoints, preprocessing state, dataset manifests, benchmark splits, system configs, frozen static weights, selected single models, governance configs, trace schemas, and release verification evidence.

### Files and Directories to Create

```text
pyproject.toml
README.md
.gitignore
configs/ch10a_import/source.yaml
configs/experiments/ch10b_robustness.yaml
external/ch10a/.gitkeep
src/mavs_ch10b/__init__.py
src/mavs_ch10b/cli.py
src/mavs_ch10b/adapters/__init__.py
src/mavs_ch10b/adapters/ch10a_source.py
src/mavs_ch10b/adapters/ch10a_artifacts.py
src/mavs_ch10b/adapters/ch10a_systems.py
src/mavs_ch10b/adapters/baseline_runner.py
src/mavs_ch10b/verification/hash_utils.py
src/mavs_ch10b/verification/import_audit.py
scripts/import_ch10a_foundation.py
scripts/run_clean_baseline.py
results/baseline_import/.gitkeep
tests/test_ch10a_import_contract.py
tests/test_no_retraining_guard.py
tests/test_clean_baseline_replay.py
tests/test_trace_schema_compatibility.py
```

### Code to Produce

- A Chapter 10A source locator that can use:
  - a local artifact repo path such as `../MAVS-Ch10A`,
  - a configured absolute path,
  - or a downloaded artifact bundle matching the Chapter 10A artifact inventory.
- A manifest validator that verifies:
  - Chapter 10A `results/reports/reproducibility_manifest.json`,
  - Chapter 10A `results/reports/artifact_inventory.json`,
  - Chapter 10A `results/reports/verification_report.md`,
  - all required dataset manifests,
  - all required processed locked and audit splits,
  - all required specialist checkpoints and metadata,
  - all required system configs,
  - all required governance trace fields.
- An import manifest written to `results/baseline_import/ch10a_import_manifest.json` containing:
  - Chapter 10A source repo URL,
  - local artifact path,
  - source git commit,
  - manifest git commit,
  - artifact inventory hash,
  - reproducibility manifest hash,
  - verification report status,
  - imported dataset ids,
  - imported specialist ids,
  - imported comparison systems,
  - checkpoint hashes,
  - config hashes,
  - split hashes.
- A clean baseline replay runner that executes every imported system on clean locked and audit benchmark splits before any corruption is applied.
- A baseline compatibility report that compares clean replay metrics against Chapter 10A reported clean metrics within an explicit tolerance.

### Coding Approach

- Treat Chapter 10A as an immutable upstream artifact.
- Use import adapters rather than copying Chapter 10A source files directly unless packaging requires a vendored snapshot.
- Pin source and artifact hashes in a Chapter 10B import manifest.
- Wrap Chapter 10A system outputs into a Chapter 10B `SystemRunBundle` so later corruption and evaluation code is not coupled to Chapter 10A internals.
- Fail closed if required artifacts are missing. Do not silently retrain, substitute models, or regenerate datasets.

### Model Handling

No model is trained in this phase.

Imported models:

- `random_forest`
- `gradient_boosted_trees`
- `mlp`

Imported systems:

- `single_model`
- `mean_ensemble`
- `static_weighted_ensemble`
- `veto_mavs`
- `pure_mavs_gc`

Imported benchmark splits:

- `locked_benchmark`
- `audit_benchmark`

### Anti-Overfitting Controls

- Phase 1 may inspect only Chapter 10A manifests, configs, clean benchmark outputs, and artifact hashes.
- No corruption grids, robustness thresholds, failure definitions, or report conclusions may be tuned based on clean replay surprises.
- The clean baseline replay exists only to verify import fidelity.
- If imported artifacts disagree with Chapter 10A manifests, stop and record the discrepancy in `Path.md`.

### Phase 1 Acceptance Criteria

- Chapter 10A source and artifact bundle are located.
- Required checkpoints, processed splits, configs, and manifests are present.
- Chapter 10A verification report is present and passes, or a blocker is recorded.
- Clean baseline replay runs for all four datasets, both benchmark splits, and all five systems.
- Clean replay metrics match Chapter 10A clean metrics within configured tolerance.
- No training command is executed.
- `Path.md` records imported artifact hashes, clean replay commands, clean replay result hashes, import deviations, and whether this phase followed the workplan.

## Phase 2 - Parameterized Corruption Engine

### Scope

Build a deterministic corruption framework that can stress the imported Chapter 10A systems without changing their training.

The corruption engine must implement every corruption family from the Chapter 10B document and the Chapter 10 research bible:

- Feature Noise
- Missing Features
- Random Feature Deletion
- Label Noise
- Confidence Distortion
- Adversarial Confidence Inflation
- Distribution Shift
- Synthetic Sensor Failure
- Specialist Failure

Each corruption must be parameterized. At minimum, every family must support a normalized corruption level from `0.0` to `1.0`, where `0.0` is the clean baseline and `1.0` is the strongest planned stress condition.

### Files and Directories to Create

```text
configs/corruptions/feature_noise.yaml
configs/corruptions/missing_features.yaml
configs/corruptions/random_feature_deletion.yaml
configs/corruptions/label_noise.yaml
configs/corruptions/confidence_distortion.yaml
configs/corruptions/adversarial_confidence_inflation.yaml
configs/corruptions/distribution_shift.yaml
configs/corruptions/synthetic_sensor_failure.yaml
configs/corruptions/specialist_failure.yaml
configs/corruptions/corruption_grid.yaml
src/mavs_ch10b/corruptions/__init__.py
src/mavs_ch10b/corruptions/base.py
src/mavs_ch10b/corruptions/feature_noise.py
src/mavs_ch10b/corruptions/missing_features.py
src/mavs_ch10b/corruptions/random_feature_deletion.py
src/mavs_ch10b/corruptions/label_noise.py
src/mavs_ch10b/corruptions/confidence_distortion.py
src/mavs_ch10b/corruptions/adversarial_confidence_inflation.py
src/mavs_ch10b/corruptions/distribution_shift.py
src/mavs_ch10b/corruptions/synthetic_sensor_failure.py
src/mavs_ch10b/corruptions/specialist_failure.py
src/mavs_ch10b/corruptions/grid.py
src/mavs_ch10b/corruptions/manifest.py
scripts/build_corruption_grid.py
results/corruption_manifests/.gitkeep
tests/test_corruption_parameterization.py
tests/test_corruption_determinism.py
tests/test_corruption_label_cleanliness.py
tests/test_corruption_bounds.py
tests/test_corruption_manifest_schema.py
```

### Code to Produce

- A common `Corruption` interface with:
  - `corruption_family`
  - `corruption_id`
  - `level`
  - `seed`
  - `target_space`
  - `apply(...)`
  - `manifest(...)`
- A grid builder that expands dataset, split, corruption family, level, and seed into immutable corruption run definitions.
- A manifest writer for every corruption run definition.
- Hashes for input bundle, corruption config, applied masks, output bundle, and random seed.
- A corruption registry that fails if a configured family is missing.

### Corruption Family Specifications

Feature Noise:

- Target: numeric feature values before specialist prediction.
- Implementation: additive and optional multiplicative noise scaled by train-side feature statistics inherited from Chapter 10A preprocessing metadata.
- Level: maps from no noise at `0.0` to the configured maximum standard deviation or range-relative perturbation at `1.0`.
- Categorical features must not receive invalid categories. If categorical corruption is added, it must be a separately recorded categorical swap mode.

Missing Features:

- Target: feature cells.
- Implementation: randomly mask a level-dependent fraction of feature cells to missing, then run the frozen Chapter 10A preprocessing transform when raw features are available, or apply processed-space missing simulation with a documented imputation proxy when only processed arrays are available.
- Level: fraction of cells masked.

Random Feature Deletion:

- Target: complete feature columns.
- Implementation: delete or mask a level-dependent fraction of feature columns for all rows in a corruption run.
- Difference from Missing Features: Missing Features is cell-level masking; Random Feature Deletion is column-level removal.
- Level: fraction of columns deleted.

Label Noise:

- Target: observed labels for evaluation stress only.
- Implementation: create `y_observed` by flipping a level-dependent fraction of labels while preserving `y_clean`.
- Metrics that require true safety, including unsafe acceptance, must use `y_clean`.
- Metrics that simulate noisy supervision or noisy audit labels may use `y_observed`, but must be labeled as observed-label metrics.

Confidence Distortion:

- Target: specialist probabilities after model prediction.
- Implementation options:
  - temperature scaling of logits,
  - additive logit bias,
  - probability compression toward `0.5`,
  - probability sharpening away from `0.5`.
- Level: distortion intensity.
- Must preserve valid probability bounds `[0, 1]`.

Adversarial Confidence Inflation:

- Target: specialist probabilities and supports.
- Implementation: inflate confidence for selected wrong or risky predictions using a deterministic adversarial rule fixed before benchmark execution.
- Level: fraction of eligible outputs modified or logit inflation strength.
- Must be reported separately from ordinary confidence distortion because it is label-aware stress.

Distribution Shift:

- Target: benchmark sample distribution.
- Implementation options:
  - class prevalence shift,
  - feature-quantile slice shift,
  - subgroup or source-row slice shift where dataset metadata permits,
  - high-severity subset sampling.
- Level: shift intensity from clean benchmark distribution to the strongest configured shifted distribution.
- Must preserve clean labels and row-id traceability.

Synthetic Sensor Failure:

- Target: semantically grouped feature blocks.
- Implementation: mask or degrade feature groups such as related numeric measurement groups, amount/time fields, or categorical blocks.
- Level: number or severity of failed feature groups.
- Must record affected feature names and group hashes.

Specialist Failure:

- Target: one or more specialist output channels.
- Implementation options:
  - specialist dropout,
  - constant `0.5` uncertainty,
  - frozen always-low or always-high output,
  - inverted output,
  - noisy output,
  - adversarially overconfident failed specialist.
- Level: number of affected specialists, probability of failure, or failure intensity.
- Must test each specialist family independently and combined failure scenarios.

### Default Corruption Grid

The initial grid should be fixed before any stress result is inspected:

```text
levels: [0.0, 0.05, 0.10, 0.20, 0.40, 0.60, 0.80, 1.0]
primary_seeds: [1001, 1002, 1003]
audit_seeds: [2001, 2002, 2003]
shadow_verification_seeds: [9001, 9002]
```

Deterministic corruptions may use one seed while still recording the seed field. Stochastic corruption metrics must aggregate over the configured primary or audit seeds.

### Coding Approach

- Separate input-space corruption from score-space corruption.
- Keep clean labels, observed labels, original feature hashes, corrupted feature hashes, original score hashes, and corrupted score hashes.
- Use deterministic random number generators seeded from dataset id, split, corruption family, level, and seed.
- Save corruption manifests before running systems.
- Never let the corruption code change model checkpoints, preprocessing state, system configs, static weights, or governance coefficients.

### Anti-Overfitting Controls

- The corruption family list, level grid, seeds, and evaluation metrics must be frozen before Phase 3 stress testing.
- Audit corruption seeds must be independent from locked corruption seeds.
- Shadow verification seeds must not influence code or config choices except to expose reproducibility failures.
- Label-aware adversarial corruption may use clean labels to construct stress, but that must be disclosed and may not be used for tuning.
- Any new corruption family added after seeing results must be marked exploratory until the full suite is rerun from frozen configs.

### Phase 2 Acceptance Criteria

- Every required corruption family is implemented and registered.
- Every corruption supports `level=0.0` and `level=1.0`.
- Every stochastic corruption is deterministic under fixed seed.
- Corruption manifests are generated for all dataset, split, level, and seed combinations.
- Tests prove bounds, determinism, label-cleanliness, manifest schema, and no mutation of frozen Chapter 10A artifacts.
- `Path.md` records every corruption file, config, grid choice, seed list, tests, generated manifest hashes, and deviations.

## Phase 3 - Governance Stress Testing Matrix

### Scope

Run all imported comparison systems through every corruption regime and produce corruption traces.

The Chapter 10B document explicitly requires:

- Mean Ensemble
- Weighted Ensemble
- Veto MAVS
- Pure MAVS-GC

The Chapter 10 research bible requires the shared Chapter 10 comparison systems, so this phase also includes:

- Single Best Model

This phase must test whether governance changes failure behavior under stress, not whether new training can improve results.

### Files and Directories to Create

```text
configs/experiments/locked_corruption_benchmark.yaml
configs/experiments/audit_corruption_benchmark.yaml
src/mavs_ch10b/stress/__init__.py
src/mavs_ch10b/stress/run_matrix.py
src/mavs_ch10b/stress/system_executor.py
src/mavs_ch10b/stress/trace_writer.py
src/mavs_ch10b/stress/cache.py
src/mavs_ch10b/stress/run_manifest.py
scripts/run_locked_corruption_benchmark.py
scripts/run_audit_corruption_benchmark.py
results/stress_runs/.gitkeep
results/corruption_traces/.gitkeep
tests/test_stress_matrix_complete.py
tests/test_systems_use_identical_corrupted_inputs.py
tests/test_all_specialists_still_speak_under_corruption.py
tests/test_corruption_trace_alignment.py
tests/test_audit_seed_independence.py
```

### Code to Produce

- A stress matrix runner that iterates over:
  - dataset,
  - benchmark split,
  - comparison system,
  - corruption family,
  - corruption level,
  - corruption seed,
  - specialist failure mode where applicable.
- A system executor that feeds identical corrupted input or score bundles to every system.
- A trace writer that records every decision for governance systems and enough prediction metadata for non-governance baselines to compare degradation.
- A run manifest that records:
  - run id,
  - run mode,
  - git commit,
  - Chapter 10A import manifest hash,
  - corruption grid hash,
  - system config hashes,
  - corruption manifest hashes,
  - output artifact hashes,
  - command line.

### Trace Requirements

Every stress trace record must include inherited MAVS-GC fields where applicable:

```text
x_id
dataset_id
split
system_id
specialist_ids
s
r
z
a
w
m
theta
R
hard_veto
decision
label
config_hash
checkpoint_hashes
trace_hash
```

Every Chapter 10B stress trace record must also include:

```text
corruption_family
corruption_id
corruption_level
corruption_seed
corruption_target_space
corruption_config_hash
corruption_manifest_hash
y_clean
y_observed
input_hash_clean
input_hash_corrupted
score_hash_clean
score_hash_corrupted
failed_specialists
feature_mask_hash
distribution_shift_descriptor
```

Fields that do not apply to a family must be present as `null`, empty lists, or empty dictionaries according to the trace schema.

### Minimum Stress Matrix

The required matrix is:

```text
4 datasets
2 benchmark splits
5 systems
9 corruption families
8 corruption levels
at least 3 independent seeds for stochastic corruption families
```

Every deterministic corruption family still records a seed and run manifest entry. Stochastic results must include seed-level rows and aggregate rows.

### Brutal Independent Testing Requirement

Every imported model and every system must be tested on benchmark data entirely different from the data used to train or configure the model:

- Imported specialists were trained on Chapter 10A train split only.
- Calibration used Chapter 10A calibration split only.
- Static weights and selected single models came from allowed Chapter 10A validation logic.
- Chapter 10B robustness evidence comes from locked and audit benchmark splits only.
- Locked corruption runs and audit corruption runs use different seeds.
- No system setting may be changed after locked corruption results are inspected unless all locked and audit results are invalidated and rerun from a new frozen configuration.

### Coding Approach

- Build clean specialist outputs once per dataset and split, then apply score-space corruptions to copies.
- For input-space corruptions, rebuild specialist outputs from corrupted inputs without saving modified checkpoints.
- Reuse Chapter 10A governance systems exactly where possible.
- Add adapter shims only for corruption metadata and trace enrichment.
- Write outputs incrementally so large corruption suites can resume without changing completed artifact hashes.

### Anti-Overfitting Controls

- The runner must refuse final mode if corruption configs are uncommitted or if the Chapter 10A import manifest changed after Phase 1.
- The runner must distinguish exploratory and final runs.
- The runner must fail if any system receives a different corrupted input bundle for the same dataset, split, family, level, and seed.
- The runner must fail if Veto MAVS or Pure MAVS-GC does not evaluate every imported specialist for every row.

### Phase 3 Acceptance Criteria

- Locked corruption benchmark runs across the full required matrix.
- Audit corruption benchmark runs across the full required matrix with independent seeds.
- Corruption traces exist for governance systems.
- Prediction outputs exist for all systems.
- Run manifests exist and include all required hashes.
- Tests prove matrix completeness, input identity across systems, all-specialists-speak behavior, trace alignment, and audit seed independence.
- `Path.md` records commands, run ids, row counts, output paths, trace hashes, any failed runs, reruns, and workplan compliance.

## Phase 4 - Robustness Evaluation and Curves

### Scope

Compute the required robustness metrics and generate `robustness_curves/`.

This phase answers how each system degrades as corruption increases and whether governance changes the safety profile of failures.

### Files and Directories to Create

```text
src/mavs_ch10b/evaluation/__init__.py
src/mavs_ch10b/evaluation/metrics.py
src/mavs_ch10b/evaluation/robustness_area.py
src/mavs_ch10b/evaluation/safety.py
src/mavs_ch10b/evaluation/aggregation.py
src/mavs_ch10b/evaluation/statistics.py
src/mavs_ch10b/evaluation/curve_builder.py
scripts/build_robustness_metrics.py
scripts/build_robustness_curves.py
results/metrics/locked_corruption/.gitkeep
results/metrics/audit_corruption/.gitkeep
results/robustness_curves/.gitkeep
results/figures/robustness_curves/.gitkeep
tests/test_robustness_metric_definitions.py
tests/test_unsafe_acceptance_metric.py
tests/test_robustness_curve_area.py
tests/test_threshold_distribution_metrics.py
tests/test_metric_trace_alignment.py
```

### Code to Produce

- Metric computation for every dataset, split, system, corruption family, level, and seed.
- Curve builders that generate metric-vs-corruption-level tables.
- Robustness curve area calculations using fixed trapezoidal integration over the configured levels.
- Aggregate tables by:
  - dataset,
  - system,
  - corruption family,
  - corruption level,
  - seed,
  - benchmark split.
- Statistical comparison tools:
  - paired bootstrap confidence intervals where row alignment permits,
  - seed-level variance,
  - locked-vs-audit consistency,
  - governance-vs-baseline deltas.

### Metric Definitions

Accuracy Under Corruption:

- `correct_decisions / evaluated_rows` using `y_clean`.

F1 Under Corruption:

- Binary F1 using `y_clean`.
- If observed-label noise metrics are reported, they must be labeled separately as observed-label F1.

Unsafe Acceptance Rate:

- Primary definition: `count(decision == 1 and y_clean == 0) / count(y_clean == 0)`.
- Also report conditional unsafe acceptance under high corruption levels and under high governance severity where applicable.

Failure Rate:

- Technical failure rate: invalid output, exception, NaN probability, missing trace, or no decision.
- Error rate `1 - accuracy` may be reported separately but must not be conflated with technical failure.

Rejection Rate:

- `count(decision == 0) / evaluated_rows`.
- For systems without explicit abstention, decision `0` is treated as rejection under the Chapter 10A binary decision convention.

Robustness Curve Area:

- Trapezoidal area over corruption levels.
- Higher is better for accuracy and F1.
- Lower is better for unsafe acceptance, technical failure, and harmful false acceptance.
- Reports must state directionality for every area metric.

Governance Severity:

- Mean, median, min, max, standard deviation, and quantiles of `a` for Veto MAVS and Pure MAVS-GC.

Governance Severity Distribution:

- Histogram or quantile table by dataset, corruption family, level, and system.

Governance Threshold Distribution:

- Histogram or quantile table of `theta` for Pure MAVS-GC and any governed threshold policy used by Veto MAVS.

### Generated Robustness Artifacts

```text
results/metrics/<split>_corruption/metric_rows.csv
results/metrics/<split>_corruption/system_summary.csv
results/metrics/<split>_corruption/governance_delta_table.csv
results/metrics/<split>_corruption/paired_bootstrap_cis.csv
results/robustness_curves/<dataset>__<system>__<corruption_family>.csv
results/robustness_curves/robustness_curve_area.csv
results/figures/robustness_curves/*.png
```

### Anti-Overfitting Controls

- Metrics must be computed from frozen stress outputs only.
- Metric definitions must be tested before report conclusions are written.
- The audit split must remain a separate robustness check and must not be averaged into locked results without preserving split labels.
- Any metric that uses `y_observed` instead of `y_clean` must be explicitly labeled.
- Reports must preserve negative and neutral results.

### Phase 4 Acceptance Criteria

- All required metrics exist for every required dataset, split, system, corruption family, level, and seed.
- Robustness curves are generated under `results/robustness_curves/`.
- Robustness curve area is computed with documented directionality.
- Governance severity and threshold distributions exist.
- Metrics align row-for-row with stress outputs and traces.
- Tests pass for metric definitions, unsafe acceptance, robustness area, threshold distributions, and trace alignment.
- `Path.md` records metric commands, artifact paths, row counts, hash summaries, test outputs, and deviations.

## Phase 5 - Analysis, Corruption Atlas, Failure Map, and Robustness Report

### Scope

Analyze the robustness results and answer the Chapter 10B research questions:

- Does governance create graceful degradation?
- Does governance suppress unsafe acceptance?
- When does MAVS fail?

Generate the final Chapter 10B outputs:

- Robustness Report
- Corruption Atlas
- Failure Map

### Files and Directories to Create

```text
configs/reports/robustness_report.yaml
src/mavs_ch10b/reporting/__init__.py
src/mavs_ch10b/reporting/tables.py
src/mavs_ch10b/reporting/figures.py
src/mavs_ch10b/reporting/corruption_atlas.py
src/mavs_ch10b/reporting/failure_map.py
src/mavs_ch10b/reporting/robustness_report.py
src/mavs_ch10b/reporting/repro_manifest.py
scripts/build_corruption_atlas.py
scripts/build_failure_map.py
scripts/build_robustness_report.py
results/reports/robustness_report.md
results/reports/corruption_atlas.md
results/reports/failure_map.md
results/reports/robustness_tables.csv
results/reports/robustness_system_deltas.csv
results/reports/robustness_reproducibility_manifest.json
results/figures/governance_severity_distribution.png
results/figures/threshold_distribution.png
results/figures/unsafe_acceptance_by_corruption.png
results/figures/robustness_area_by_system.png
tests/test_report_inputs_complete.py
tests/test_report_claims_reference_artifacts.py
tests/test_corruption_atlas_complete.py
tests/test_failure_map_complete.py
```

### Code to Produce

- Robustness tables:
  - dataset x split x system x corruption family x level x seed x metric.
  - governance deltas against Single Best Model, Mean Ensemble, Static Weighted Ensemble, and Veto MAVS.
  - locked-vs-audit consistency tables.
  - robustness curve area comparisons.
- Robustness figures:
  - robustness curves by corruption family,
  - unsafe acceptance by corruption family,
  - rejection rate by corruption level,
  - governance severity distribution,
  - threshold distribution,
  - failure-rate heatmaps,
  - robustness area by system.
- Corruption Atlas:
  - one section per corruption family,
  - implementation definition,
  - parameterization,
  - affected target space,
  - expected failure mode,
  - observed degradation patterns,
  - best and worst systems,
  - linked artifacts.
- Failure Map:
  - when Pure MAVS-GC fails,
  - when Veto MAVS fails,
  - when governance over-rejects,
  - when governance under-rejects,
  - when unsafe acceptance survives,
  - which corruption families are most damaging,
  - whether failures are specialist-driven, feature-driven, confidence-driven, label-driven, or governance-policy-driven.
- Robustness Report:
  - source documents and mission,
  - Chapter 10A dependency and import fidelity,
  - methods,
  - corruption grid,
  - systems,
  - benchmark protocol,
  - anti-overfitting controls,
  - results,
  - limitations,
  - final answer to Chapter 10B.

### Analysis Rules

- Do not claim universal robustness superiority unless supported across multiple datasets, multiple corruptions, and multiple baselines.
- Distinguish Pure MAVS-GC from Veto MAVS; Veto MAVS is a governance control, not an aggregation-only baseline.
- If MAVS-GC improves unsafe acceptance but hurts accuracy or recall, state the tradeoff plainly.
- If MAVS-GC over-rejects, state that plainly.
- If governance severity rises under corruption but does not improve safety, state that the severity signal alone is insufficient.
- Negative and neutral evidence must be retained as first-class research evidence.
- The final answer must separate:
  - graceful degradation,
  - unsafe acceptance suppression,
  - technical failure,
  - rejection behavior,
  - threshold/severity behavior.

### Anti-Overfitting Controls

- The report must identify final vs exploratory runs.
- The report must include locked and audit split results separately.
- The report must include the corruption seed protocol.
- The report must include config and artifact hashes.
- No report conclusion may depend on a run missing from the reproducibility manifest.
- Claims must link to generated tables, figures, or trace-derived metrics.

### Phase 5 Acceptance Criteria

- Robustness Report exists and answers the research question.
- Corruption Atlas exists and covers every required corruption family.
- Failure Map exists and identifies MAVS failure modes.
- Robustness tables, deltas, figures, and reproducibility manifest exist.
- Every claim maps to benchmark artifacts.
- `Path.md` records report generation commands, artifact hashes, claim support, limitations, and workplan compliance.

## Phase 6 - Verification, Reproduction, and Release Readiness

### Scope

Perform final end-to-end verification so the repository can serve as the Chapter 10B robustness artifact.

This phase ensures the evidence is reproducible, statistically supported, observed across multiple datasets, observed against multiple baselines, and documented through traces and reports.

### Files and Directories to Create

```text
scripts/reproduce_all.py
scripts/hash_artifacts.py
scripts/verify_artifacts.py
results/reports/artifact_inventory.json
results/reports/verification_report.md
tests/test_end_to_end_smoke.py
tests/test_artifact_inventory_complete.py
tests/test_final_run_guards.py
```

### Code to Produce

- One-command reproduction script:
  - import Chapter 10A foundation,
  - run clean baseline replay,
  - build corruption grid,
  - run locked corruption benchmark,
  - run audit corruption benchmark,
  - build robustness metrics,
  - build robustness curves,
  - build Corruption Atlas,
  - build Failure Map,
  - build Robustness Report,
  - hash artifacts,
  - verify artifacts.
- Artifact inventory:
  - documentation,
  - configs,
  - source,
  - tests,
  - scripts,
  - import manifests,
  - corruption manifests,
  - stress run manifests,
  - metric tables,
  - robustness curves,
  - figures,
  - reports.
- Verification gate:
  - required files exist,
  - hashes match,
  - Chapter 10A import passed,
  - no retraining was performed,
  - corruption grid is complete,
  - stress matrix is complete,
  - locked and audit seeds are independent,
  - metrics cover all required systems and corruptions,
  - governance traces contain all required fields,
  - reports reference existing artifacts,
  - `Path.md` records all phase evidence.

### Anti-Overfitting Controls

- Final verification must fail if any final run used exploratory mode.
- Final verification must fail if configs changed after run manifests were written.
- Final verification must fail if Chapter 10A import artifacts changed after Phase 1.
- Final verification must fail if audit corruption seeds overlap with locked corruption seeds.
- Final verification must fail if model training artifacts are created by Chapter 10B final commands.

### Phase 6 Acceptance Criteria

- `python scripts/reproduce_all.py --run-mode final` succeeds from a prepared checkout with access to Chapter 10A artifacts.
- Artifact inventory is complete.
- Verification report has overall status `pass`.
- Test suite passes.
- `Path.md` contains the complete implementation trail from source review through final verification.

## Required Benchmark Matrix

Datasets:

```text
breast_cancer_wisconsin
adult_income
credit_card_fraud
bank_marketing
```

Specialists:

```text
random_forest
gradient_boosted_trees
mlp
```

Systems:

```text
single_model
mean_ensemble
static_weighted_ensemble
veto_mavs
pure_mavs_gc
```

Splits:

```text
locked_benchmark
audit_benchmark
```

Corruption families:

```text
feature_noise
missing_features
random_feature_deletion
label_noise
confidence_distortion
adversarial_confidence_inflation
distribution_shift
synthetic_sensor_failure
specialist_failure
```

Metrics:

```text
accuracy_under_corruption
f1_under_corruption
unsafe_acceptance_rate
failure_rate
rejection_rate
robustness_curve_area
governance_severity
governance_severity_distribution
governance_threshold_distribution
```

Minimum deterministic metric cells before seed expansion:

```text
4 datasets * 2 splits * 5 systems * 9 corruption families * 8 levels = 2880 system-level corruption cells
```

Stochastic corruption families must retain seed-level outputs and aggregate outputs.

## Chapter 10B Trace Contract

Governance stress traces must preserve MAVS-GC interpretability and add corruption provenance. Required trace fields:

```text
x_id
dataset_id
split
system_id
specialist_ids
s
r
z
a
w
m
theta
R
hard_veto
decision
label
y_clean
y_observed
corruption_family
corruption_id
corruption_level
corruption_seed
corruption_target_space
corruption_config_hash
corruption_manifest_hash
input_hash_clean
input_hash_corrupted
score_hash_clean
score_hash_corrupted
failed_specialists
feature_mask_hash
distribution_shift_descriptor
config_hash
checkpoint_hashes
trace_hash
```

Required trace tests:

- All specialists speak under every corruption unless the corruption explicitly simulates a specialist failure, in which case the failed specialist must still be represented in trace metadata.
- Increasing corruption level does not mutate frozen model or system artifacts.
- Hard veto remains honored under corrupted confidence and maximum mitigation.
- Trace output is deterministic for fixed inputs, configs, seeds, checkpoints, and preprocessing.
- Corruption provenance hashes are stable and reproducible.

## Path.md Documentation Contract

`Path.md` must be updated as implementation proceeds. Each material update must include:

- date and local time,
- phase,
- files created or changed,
- code produced,
- commands run,
- datasets touched,
- models imported, trained, or evaluated,
- corruption families touched,
- benchmark or test outputs,
- artifact hashes,
- whether the work followed this WorkPlan,
- deviations and reason,
- risks or limitations,
- next required action.

No phase is complete until `Path.md` contains enough evidence to verify that phase against this workplan.

