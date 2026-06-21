# Corruption Atlas

This atlas covers every required Chapter 10B corruption family. Each section links implementation definition, parameterization, target space, expected failure mode, observed degradation, best and worst systems, and artifacts.

Evidence source: `results/metrics/*_corruption/metric_rows.csv`, `results/robustness_curves/robustness_curve_area.csv`, and `results/corruption_manifests/corruption_grid_manifest.json`.

## adversarial_confidence_inflation

### Implementation Definition

Label-aware inflation of wrong specialist confidence for adversarial stress.

### Parameterization

- `epsilon`: `1e-06`
- `max_eligible_fraction`: `1.0`
- `max_inflation_strength`: `0.95`

### Affected Target Space

- Config target space: `scores`
- Observed target space in metric rows: `scores`
- Failure class: `confidence-driven`

### Expected Failure Mode

Confidence inflation tests false certainty and unsafe acceptance pressure.

### Observed Degradation Pattern

- Mean accuracy across all systems: `0.927471`.
- Mean unsafe acceptance across all systems: `0.030381`.
- Mean rejection rate across all systems: `0.841951`.
- Best average accuracy system: `Single Best Model` with `0.932411`.
- Lowest unsafe acceptance system: `Pure MAVS-GC` with `0.024861`.
- Highest rejection system: `Pure MAVS-GC` with `0.853532`.

### Best and Worst Systems

- Best accuracy area system: `Single Best Model`.
- Worst average accuracy system: `Pure MAVS-GC` with `0.925016`.

### Linked Artifacts

- Locked metric rows: `results/metrics/locked_corruption/metric_rows.csv`
- Audit metric rows: `results/metrics/audit_corruption/metric_rows.csv`
- Robustness area table: `results/robustness_curves/robustness_curve_area.csv`
- Example curve CSV: `results/robustness_curves/breast_cancer_wisconsin__single_model__adversarial_confidence_inflation.csv`

## confidence_distortion

### Implementation Definition

Temperature-style probability compression toward uncertainty.

### Parameterization

- `epsilon`: `1e-06`
- `max_temperature`: `5.0`

### Affected Target Space

- Config target space: `scores`
- Observed target space in metric rows: `scores`
- Failure class: `confidence-driven`

### Expected Failure Mode

Probability compression tests whether governance severity reacts to weaker confidence separation.

### Observed Degradation Pattern

- Mean accuracy across all systems: `0.931003`.
- Mean unsafe acceptance across all systems: `0.026495`.
- Mean rejection rate across all systems: `0.844599`.
- Best average accuracy system: `Static Weighted Ensemble` with `0.932906`.
- Lowest unsafe acceptance system: `Pure MAVS-GC` with `0.014144`.
- Highest rejection system: `Pure MAVS-GC` with `0.866934`.

### Best and Worst Systems

- Best accuracy area system: `Static Weighted Ensemble`.
- Worst average accuracy system: `Pure MAVS-GC` with `0.928122`.

### Linked Artifacts

- Locked metric rows: `results/metrics/locked_corruption/metric_rows.csv`
- Audit metric rows: `results/metrics/audit_corruption/metric_rows.csv`
- Robustness area table: `results/robustness_curves/robustness_curve_area.csv`
- Example curve CSV: `results/robustness_curves/breast_cancer_wisconsin__single_model__confidence_distortion.csv`

## distribution_shift

### Implementation Definition

Feature-norm shift by deterministic row subset selection while preserving row ids and clean labels.

### Parameterization

- `min_retention_fraction`: `0.35`
- `score_mode`: `feature_norm`

### Affected Target Space

- Config target space: `rows`
- Observed target space in metric rows: `rows`
- Failure class: `feature-driven distribution-shift`

### Expected Failure Mode

Subset shift changes benchmark composition and tests out-of-distribution sensitivity.

### Observed Degradation Pattern

- Mean accuracy across all systems: `0.932189`.
- Mean unsafe acceptance across all systems: `0.030313`.
- Mean rejection rate across all systems: `0.801164`.
- Best average accuracy system: `Static Weighted Ensemble` with `0.933701`.
- Lowest unsafe acceptance system: `Pure MAVS-GC` with `0.022075`.
- Highest rejection system: `Pure MAVS-GC` with `0.815626`.

### Best and Worst Systems

- Best accuracy area system: `Static Weighted Ensemble`.
- Worst average accuracy system: `Pure MAVS-GC` with `0.930873`.

### Linked Artifacts

- Locked metric rows: `results/metrics/locked_corruption/metric_rows.csv`
- Audit metric rows: `results/metrics/audit_corruption/metric_rows.csv`
- Robustness area table: `results/robustness_curves/robustness_curve_area.csv`
- Example curve CSV: `results/robustness_curves/breast_cancer_wisconsin__single_model__distribution_shift.csv`

## feature_noise

### Implementation Definition

Additive processed-feature noise scaled by train-side feature statistics when available.

### Parameterization

- `finite_clip`: `1000000.0`
- `max_std_multiplier`: `1.0`
- `mode`: `additive_gaussian`

### Affected Target Space

- Config target space: `features`
- Observed target space in metric rows: `features`
- Failure class: `feature-driven`

### Expected Failure Mode

Processed features move away from the Chapter 10A train distribution while preserving clean labels.

### Observed Degradation Pattern

- Mean accuracy across all systems: `0.920344`.
- Mean unsafe acceptance across all systems: `0.035583`.
- Mean rejection rate across all systems: `0.842599`.
- Best average accuracy system: `Mean Ensemble` with `0.920908`.
- Lowest unsafe acceptance system: `Pure MAVS-GC` with `0.023004`.
- Highest rejection system: `Pure MAVS-GC` with `0.861370`.

### Best and Worst Systems

- Best accuracy area system: `Pure MAVS-GC`.
- Worst average accuracy system: `Single Best Model` with `0.918797`.

### Linked Artifacts

- Locked metric rows: `results/metrics/locked_corruption/metric_rows.csv`
- Audit metric rows: `results/metrics/audit_corruption/metric_rows.csv`
- Robustness area table: `results/robustness_curves/robustness_curve_area.csv`
- Example curve CSV: `results/robustness_curves/breast_cancer_wisconsin__single_model__feature_noise.csv`

## label_noise

### Implementation Definition

Observed-label flips for evaluation stress while preserving clean labels.

### Parameterization

- `max_flip_fraction`: `1.0`

### Affected Target Space

- Config target space: `labels`
- Observed target space in metric rows: `labels`
- Failure class: `label-driven`

### Expected Failure Mode

Observed-label corruption tests metric hygiene; clean labels remain the final authority.

### Observed Degradation Pattern

- Mean accuracy across all systems: `0.931417`.
- Mean unsafe acceptance across all systems: `0.027842`.
- Mean rejection rate across all systems: `0.842175`.
- Best average accuracy system: `Static Weighted Ensemble` with `0.932909`.
- Lowest unsafe acceptance system: `Pure MAVS-GC` with `0.021000`.
- Highest rejection system: `Pure MAVS-GC` with `0.854761`.

### Best and Worst Systems

- Best accuracy area system: `Static Weighted Ensemble`.
- Worst average accuracy system: `Pure MAVS-GC` with `0.930053`.

### Linked Artifacts

- Locked metric rows: `results/metrics/locked_corruption/metric_rows.csv`
- Audit metric rows: `results/metrics/audit_corruption/metric_rows.csv`
- Robustness area table: `results/robustness_curves/robustness_curve_area.csv`
- Example curve CSV: `results/robustness_curves/breast_cancer_wisconsin__single_model__label_noise.csv`

## missing_features

### Implementation Definition

Cell-level processed-feature masking with deterministic fill value.

### Parameterization

- `fill_value`: `0.0`
- `max_missing_fraction`: `1.0`

### Affected Target Space

- Config target space: `features`
- Observed target space in metric rows: `features`
- Failure class: `feature-driven`

### Expected Failure Mode

Feature absence forces specialists and governance to operate with incomplete evidence.

### Observed Degradation Pattern

- Mean accuracy across all systems: `0.899579`.
- Mean unsafe acceptance across all systems: `0.018295`.
- Mean rejection rate across all systems: `0.889639`.
- Best average accuracy system: `Static Weighted Ensemble` with `0.902194`.
- Lowest unsafe acceptance system: `Pure MAVS-GC` with `0.010340`.
- Highest rejection system: `Pure MAVS-GC` with `0.905223`.

### Best and Worst Systems

- Best accuracy area system: `Static Weighted Ensemble`.
- Worst average accuracy system: `Pure MAVS-GC` with `0.895757`.

### Linked Artifacts

- Locked metric rows: `results/metrics/locked_corruption/metric_rows.csv`
- Audit metric rows: `results/metrics/audit_corruption/metric_rows.csv`
- Robustness area table: `results/robustness_curves/robustness_curve_area.csv`
- Example curve CSV: `results/robustness_curves/breast_cancer_wisconsin__single_model__missing_features.csv`

## random_feature_deletion

### Implementation Definition

Column-level processed-feature deletion with deterministic fill value.

### Parameterization

- `fill_value`: `0.0`
- `max_deletion_fraction`: `1.0`

### Affected Target Space

- Config target space: `features`
- Observed target space in metric rows: `features`
- Failure class: `feature-driven`

### Expected Failure Mode

Random feature removal tests whether decisions depend on brittle individual coordinates.

### Observed Degradation Pattern

- Mean accuracy across all systems: `0.900347`.
- Mean unsafe acceptance across all systems: `0.019988`.
- Mean rejection rate across all systems: `0.886395`.
- Best average accuracy system: `Static Weighted Ensemble` with `0.902460`.
- Lowest unsafe acceptance system: `Pure MAVS-GC` with `0.011483`.
- Highest rejection system: `Pure MAVS-GC` with `0.903454`.

### Best and Worst Systems

- Best accuracy area system: `Static Weighted Ensemble`.
- Worst average accuracy system: `Pure MAVS-GC` with `0.895932`.

### Linked Artifacts

- Locked metric rows: `results/metrics/locked_corruption/metric_rows.csv`
- Audit metric rows: `results/metrics/audit_corruption/metric_rows.csv`
- Robustness area table: `results/robustness_curves/robustness_curve_area.csv`
- Example curve CSV: `results/robustness_curves/breast_cancer_wisconsin__single_model__random_feature_deletion.csv`

## specialist_failure

### Implementation Definition

Specialist output channel failure while retaining specialist trace representation.

### Parameterization

- `failure_mode`: `constant_uncertainty`
- `uncertainty_probability`: `0.5`

### Affected Target Space

- Config target space: `scores`
- Observed target space in metric rows: `scores`
- Failure class: `specialist-driven`

### Expected Failure Mode

Specialist failure tests whether a damaged specialist can dominate or destabilize governance.

### Observed Degradation Pattern

- Mean accuracy across all systems: `0.745068`.
- Mean unsafe acceptance across all systems: `0.257094`.
- Mean rejection rate across all systems: `0.648744`.
- Best average accuracy system: `Pure MAVS-GC` with `0.899467`.
- Lowest unsafe acceptance system: `Pure MAVS-GC` with `0.013527`.
- Highest rejection system: `Pure MAVS-GC` with `0.896851`.

### Best and Worst Systems

- Best accuracy area system: `Pure MAVS-GC`.
- Worst average accuracy system: `Single Best Model` with `0.594636`.

### Linked Artifacts

- Locked metric rows: `results/metrics/locked_corruption/metric_rows.csv`
- Audit metric rows: `results/metrics/audit_corruption/metric_rows.csv`
- Robustness area table: `results/robustness_curves/robustness_curve_area.csv`
- Example curve CSV: `results/robustness_curves/breast_cancer_wisconsin__single_model__specialist_failure.csv`

## synthetic_sensor_failure

### Implementation Definition

Feature-group sensor failure using deterministic contiguous feature groups.

### Parameterization

- `fill_value`: `0.0`
- `max_groups`: `5`

### Affected Target Space

- Config target space: `features`
- Observed target space in metric rows: `features`
- Failure class: `feature-driven sensor-failure`

### Expected Failure Mode

Structured sensor-style failure tests correlated feature degradation.

### Observed Degradation Pattern

- Mean accuracy across all systems: `0.895335`.
- Mean unsafe acceptance across all systems: `0.019840`.
- Mean rejection rate across all systems: `0.892271`.
- Best average accuracy system: `Mean Ensemble` with `0.897472`.
- Lowest unsafe acceptance system: `Pure MAVS-GC` with `0.010195`.
- Highest rejection system: `Pure MAVS-GC` with `0.906941`.

### Best and Worst Systems

- Best accuracy area system: `Mean Ensemble`.
- Worst average accuracy system: `Single Best Model` with `0.893420`.

### Linked Artifacts

- Locked metric rows: `results/metrics/locked_corruption/metric_rows.csv`
- Audit metric rows: `results/metrics/audit_corruption/metric_rows.csv`
- Robustness area table: `results/robustness_curves/robustness_curve_area.csv`
- Example curve CSV: `results/robustness_curves/breast_cancer_wisconsin__single_model__synthetic_sensor_failure.csv`
