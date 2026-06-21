# MAVS Chapter 10B Robustness Report

## Source Documents and Mission

This report is grounded in the Chapter 10B workplan source authority: `MAVS Chapter 10B.pdf`, `Mavs.pdf`, `Mavs Research Bible - Chapter 10.pdf`, and `MAVS Research Bible - Chapter 10A Completion Report.pdf`.

Mission question: Does MAVS-GC fail more safely under adverse conditions?

## Chapter 10A Dependency and Import Fidelity

Chapter 10B imports the completed Chapter 10A foundation and performs no model training. The Phase 1 import report records Chapter 10A verification status `pass`; Phase 5 uses only generated Phase 3 and Phase 4 benchmark artifacts.

## Methods

- Datasets: `adult_income, bank_marketing, breast_cancer_wisconsin, credit_card_fraud`.
- Systems: `mean_ensemble, pure_mavs_gc, single_model, static_weighted_ensemble, veto_mavs`.
- Corruption families: `adversarial_confidence_inflation, confidence_distortion, distribution_shift, feature_noise, label_noise, missing_features, random_feature_deletion, specialist_failure, synthetic_sensor_failure`.
- Corruption levels: `0.0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0`.
- Metric rows analyzed: `14400`.
- Robustness area rows analyzed: `3600`.

## Benchmark Protocol

Locked and audit benchmark splits are reported separately in `results/reports/robustness_tables.csv`. Locked uses the primary and shadow seed roles; audit uses audit and shadow seed roles. Shadow seeds are retained as verification stress evidence and are not used for tuning.

## Anti-Overfitting Controls

- Run modes observed in Phase 4 metric rows: `exploratory`.
- No Phase 5 code trains or tunes models, thresholds, weights, corruption levels, or seeds.
- Conclusions are tied to claim IDs and artifact paths in `results/reports/robustness_reproducibility_manifest.json`.
- The report does not claim universal robustness superiority because the evidence contains tradeoffs and negative cases.

## Results

- Pure MAVS-GC overall mean accuracy: `0.913418`.
- Pure MAVS-GC overall mean unsafe acceptance: `0.016737`.
- Pure MAVS-GC overall mean rejection rate: `0.873855`.
- Pure MAVS-GC vs Veto MAVS mean accuracy delta: `0.015589`.
- Pure MAVS-GC vs Veto MAVS mean unsafe acceptance delta: `-0.036608`.
- Pure MAVS-GC vs Veto MAVS mean rejection delta: `0.043603`.
- Veto MAVS vs Mean Ensemble mean accuracy delta: `0.000000`.
- Most damaging corruption family by mean accuracy: `specialist_failure` with `0.745068`.
- High-corruption Pure MAVS-GC mean unsafe acceptance: `0.013733`.

## Final Answer to Chapter 10B

The current exploratory evidence supports a qualified answer: Pure MAVS-GC often fails more safely by suppressing unsafe acceptance, especially against specialist failure, but it does so by increasing rejection and can produce severe over-rejection. Graceful degradation is not universal. Veto MAVS functions as a governance control in trace structure, but in these artifacts it does not materially change mean-ensemble decisions. MAVS failure modes are therefore not eliminated; they are shifted among unsafe acceptance, rejection, and accuracy/F1 loss.

## Limitations

- The full Phase 3 stress runs are marked `exploratory`; final release-mode verification is Phase 6 work.
- Veto MAVS and Mean Ensemble are decision-identical in these artifacts, so Veto MAVS should not be treated as evidence of improved robustness here.
- Pure MAVS-GC safety improvements are coupled to rejection behavior and cannot be reported as free predictive improvement.
- Claims are limited to the four Chapter 10A datasets and the configured corruption grid.

## Figures

- `results/figures/governance_severity_distribution.png` sha256 `b41fe3ee079f4a983b1f4b1a440e26cce7470a9b8c45e46b8b90a833cb848975`
- `results/figures/threshold_distribution.png` sha256 `438908ed9cfb9fdaa9c7b2dd8091d9eedc4ee9d043b8026dbe639a5499a8f84e`
- `results/figures/unsafe_acceptance_by_corruption.png` sha256 `3fb02385f81474e7f0febfcb41be36442d4efcceba6b7daa6342f4874c3ef7b4`
- `results/figures/robustness_area_by_system.png` sha256 `f67ef92292f53168df0c3084c5fb2d00fac944bd3e50c78eff677dc63231f5d3`
- `results/figures/rejection_rate_by_corruption.png` sha256 `1214a0aec294267d8439dab2e3d445db7238a458d3e7baa8d896d67293f4139e`
- `results/figures/failure_rate_heatmap.png` sha256 `d22132b5eeb2ee269e376da927f51ca853ab799cf76b82f03cd67eb194d4d1fc`

## Claim Support Ledger

- `CLAIM-P5-001`: The Phase 5 report analyzes exploratory locked and audit stress runs, not final release-mode runs. Support: `results/metrics/locked_corruption/metric_rows.csv`, `results/metrics/audit_corruption/metric_rows.csv`, `results/reports/robustness_tables.csv`.
- `CLAIM-P5-002`: Pure MAVS-GC suppresses unsafe acceptance relative to Veto MAVS on average, with mean unsafe delta -0.036608. Support: `results/reports/robustness_system_deltas.csv`, `results/reports/robustness_tables.csv`, `results/figures/unsafe_acceptance_by_corruption.png`.
- `CLAIM-P5-003`: Pure MAVS-GC increases rejection relative to Veto MAVS on average, with mean rejection delta 0.043603. Support: `results/reports/robustness_system_deltas.csv`, `results/reports/failure_map.md`.
- `CLAIM-P5-004`: Veto MAVS does not change the mean ensemble decision stream in the current artifacts; average accuracy delta is 0.000000. Support: `results/reports/robustness_system_deltas.csv`, `results/reports/failure_map.md`.
- `CLAIM-P5-005`: The most damaging corruption family by mean accuracy is specialist_failure with mean accuracy 0.745068. Support: `results/reports/robustness_tables.csv`, `results/reports/corruption_atlas.md`, `results/reports/failure_map.md`.
- `CLAIM-P5-006`: Pure MAVS-GC has the lowest overall unsafe acceptance mean among systems, 0.016737, but this is paired with high rejection. Support: `results/reports/robustness_tables.csv`, `results/reports/robustness_system_deltas.csv`, `results/reports/failure_map.md`.
- `CLAIM-P5-007`: Technical failure rate is zero in the generated metric rows; observed failures are decision-quality and rejection-behavior failures. Support: `results/reports/robustness_tables.csv`, `results/metrics/locked_corruption/metric_rows.csv`, `results/metrics/audit_corruption/metric_rows.csv`.
- `CLAIM-P5-008`: Governance severity and threshold behavior are reported as trace-derived evidence, not as proof of safety by themselves. Support: `results/figures/governance_severity_distribution.png`, `results/metrics/locked_corruption/governance_severity_distribution.csv`, `results/metrics/audit_corruption/governance_threshold_distribution.csv`.

## Linked Final Artifacts

- Robustness tables: `results/reports/robustness_tables.csv`
- System deltas: `results/reports/robustness_system_deltas.csv`
- Corruption Atlas: `results/reports/corruption_atlas.md`
- Failure Map: `results/reports/failure_map.md`
- Reproducibility manifest: `results/reports/robustness_reproducibility_manifest.json`
