# Failure Map

This map identifies where MAVS governance fails, where it suppresses unsafe acceptance, and where it shifts errors into rejection. All evidence is from locked and audit Phase 4 metric artifacts.

## Executive Failure Summary

- Most damaging corruption family by mean accuracy: `specialist_failure` with mean accuracy `0.745068`.
- Pure MAVS-GC vs Veto MAVS average accuracy delta: `0.015589`.
- Pure MAVS-GC vs Veto MAVS average unsafe acceptance delta: `-0.036608`.
- Pure MAVS-GC vs Veto MAVS average rejection-rate delta: `0.043603`.
- Veto MAVS vs Mean Ensemble average accuracy delta: `0.000000`.
- Veto MAVS vs Mean Ensemble average unsafe acceptance delta: `0.000000`.

## When Pure MAVS-GC Fails

Pure MAVS-GC fails primarily by over-rejection in the observed artifacts. Its lowest-accuracy rows often have `rejection_rate = 1.0`, which suppresses unsafe acceptance but can destroy F1.

| split_label | dataset_id | corruption_family | corruption_level | seed_role | corruption_seed | accuracy | f1 | unsafe_acceptance_rate | rejection_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| audit | breast_cancer_wisconsin | missing_features | 1.000000 | audit | 2001 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | missing_features | 1.000000 | audit | 2002 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | missing_features | 1.000000 | audit | 2003 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | missing_features | 1.000000 | shadow | 9001 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | missing_features | 1.000000 | shadow | 9002 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | random_feature_deletion | 0.800000 | audit | 2001 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | random_feature_deletion | 0.800000 | audit | 2002 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | random_feature_deletion | 1.000000 | audit | 2001 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |

## When Veto MAVS Fails

Veto MAVS fails when the veto control does not change the mean-ensemble decision stream. In the generated deltas, Veto MAVS and Mean Ensemble have zero average delta for the primary metrics.

| split_label | dataset_id | corruption_family | corruption_level | seed_role | corruption_seed | accuracy | f1 | unsafe_acceptance_rate | rejection_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| audit | credit_card_fraud | specialist_failure | 1.000000 | shadow | 9002 | 0.001756 | 0.003505 | 1.000000 | 0.000000 |
| audit | credit_card_fraud | specialist_failure | 1.000000 | shadow | 9001 | 0.001756 | 0.003505 | 1.000000 | 0.000000 |
| audit | credit_card_fraud | specialist_failure | 1.000000 | audit | 2003 | 0.001756 | 0.003505 | 1.000000 | 0.000000 |
| audit | credit_card_fraud | specialist_failure | 1.000000 | audit | 2002 | 0.001756 | 0.003505 | 1.000000 | 0.000000 |
| audit | credit_card_fraud | specialist_failure | 1.000000 | audit | 2001 | 0.001756 | 0.003505 | 1.000000 | 0.000000 |
| audit | credit_card_fraud | specialist_failure | 0.800000 | shadow | 9002 | 0.001756 | 0.003505 | 1.000000 | 0.000000 |
| audit | credit_card_fraud | specialist_failure | 0.800000 | shadow | 9001 | 0.001756 | 0.003505 | 1.000000 | 0.000000 |
| locked | credit_card_fraud | specialist_failure | 1.000000 | shadow | 9002 | 0.001720 | 0.003435 | 1.000000 | 0.000000 |

## Governance Over-Rejection

Over-rejection is recorded where governance systems reject at least 95 percent of evaluated rows. This is a safety tradeoff, not a free robustness improvement.

| split_label | dataset_id | system_id | corruption_family | corruption_level | seed_role | corruption_seed | accuracy | f1 | unsafe_acceptance_rate | rejection_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| audit | breast_cancer_wisconsin | veto_mavs | missing_features | 1.000000 | audit | 2001 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | pure_mavs_gc | missing_features | 1.000000 | audit | 2001 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | veto_mavs | missing_features | 1.000000 | audit | 2002 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | pure_mavs_gc | missing_features | 1.000000 | audit | 2002 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | veto_mavs | missing_features | 1.000000 | audit | 2003 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | pure_mavs_gc | missing_features | 1.000000 | audit | 2003 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | veto_mavs | missing_features | 1.000000 | shadow | 9001 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | pure_mavs_gc | missing_features | 1.000000 | shadow | 9001 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | veto_mavs | missing_features | 1.000000 | shadow | 9002 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | pure_mavs_gc | missing_features | 1.000000 | shadow | 9002 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | pure_mavs_gc | random_feature_deletion | 0.800000 | audit | 2001 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |
| audit | breast_cancer_wisconsin | pure_mavs_gc | random_feature_deletion | 0.800000 | audit | 2002 | 0.620690 | 0.000000 | 0.000000 | 1.000000 |

## Governance Under-Rejection

Under-rejection is recorded where unsafe acceptance is at least 50 percent while rejection is at most 10 percent.

| split_label | dataset_id | system_id | corruption_family | corruption_level | seed_role | corruption_seed | accuracy | f1 | unsafe_acceptance_rate | rejection_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 0.800000 | primary | 1001 | 0.368421 | 0.538462 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 0.800000 | primary | 1002 | 0.368421 | 0.538462 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 0.800000 | primary | 1003 | 0.368421 | 0.538462 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 0.800000 | shadow | 9001 | 0.368421 | 0.538462 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 0.800000 | shadow | 9002 | 0.368421 | 0.538462 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 1.000000 | primary | 1001 | 0.368421 | 0.538462 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 1.000000 | primary | 1002 | 0.368421 | 0.538462 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 1.000000 | primary | 1003 | 0.368421 | 0.538462 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 1.000000 | shadow | 9001 | 0.368421 | 0.538462 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 1.000000 | shadow | 9002 | 0.368421 | 0.538462 | 1.000000 | 0.000000 |
| locked | adult_income | veto_mavs | specialist_failure | 0.800000 | primary | 1001 | 0.239353 | 0.386255 | 1.000000 | 0.000000 |
| locked | adult_income | veto_mavs | specialist_failure | 0.800000 | primary | 1002 | 0.239353 | 0.386255 | 1.000000 | 0.000000 |

## Unsafe Acceptance Survives

Unsafe acceptance still survives in governance systems under severe specialist failure and confidence stress cases.

| split_label | dataset_id | system_id | corruption_family | corruption_level | seed_role | corruption_seed | unsafe_acceptance_rate | rejection_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 0.800000 | primary | 1001 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 0.800000 | primary | 1002 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 1.000000 | primary | 1003 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 1.000000 | primary | 1002 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 1.000000 | primary | 1001 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 0.800000 | shadow | 9002 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 0.800000 | shadow | 9001 | 1.000000 | 0.000000 |
| locked | breast_cancer_wisconsin | veto_mavs | specialist_failure | 0.800000 | primary | 1003 | 1.000000 | 0.000000 |
| locked | adult_income | veto_mavs | specialist_failure | 1.000000 | shadow | 9001 | 1.000000 | 0.000000 |
| locked | adult_income | veto_mavs | specialist_failure | 1.000000 | shadow | 9002 | 1.000000 | 0.000000 |
| locked | credit_card_fraud | veto_mavs | specialist_failure | 0.800000 | primary | 1001 | 1.000000 | 0.000000 |
| locked | credit_card_fraud | veto_mavs | specialist_failure | 0.800000 | primary | 1002 | 1.000000 | 0.000000 |

## Most Damaging Corruption Families

| corruption_family | accuracy | f1 | unsafe_acceptance_rate | rejection_rate |
| --- | --- | --- | --- | --- |
| specialist_failure | 0.745068 | 0.580386 | 0.257094 | 0.648744 |
| synthetic_sensor_failure | 0.895335 | 0.422548 | 0.019840 | 0.892271 |
| missing_features | 0.899579 | 0.483105 | 0.018295 | 0.889639 |
| random_feature_deletion | 0.900347 | 0.470783 | 0.019988 | 0.886395 |
| feature_noise | 0.920344 | 0.691902 | 0.035583 | 0.842599 |
| adversarial_confidence_inflation | 0.927471 | 0.714963 | 0.030381 | 0.841951 |
| confidence_distortion | 0.931003 | 0.722767 | 0.026495 | 0.844599 |
| label_noise | 0.931417 | 0.728504 | 0.027842 | 0.842175 |
| distribution_shift | 0.932189 | 0.756959 | 0.030313 | 0.801164 |

## Failure Mechanism Classification

- `adversarial_confidence_inflation`: `confidence-driven`.
- `confidence_distortion`: `confidence-driven`.
- `distribution_shift`: `feature-driven distribution-shift`.
- `feature_noise`: `feature-driven`.
- `label_noise`: `label-driven`.
- `missing_features`: `feature-driven`.
- `random_feature_deletion`: `feature-driven`.
- `specialist_failure`: `specialist-driven`.
- `synthetic_sensor_failure`: `feature-driven sensor-failure`.

## Linked Artifacts

- Robustness tables: `results/reports/robustness_tables.csv`
- System deltas: `results/reports/robustness_system_deltas.csv`
- Locked metric rows: `results/metrics/locked_corruption/metric_rows.csv`
- Audit metric rows: `results/metrics/audit_corruption/metric_rows.csv`
- Unsafe acceptance figure: `results/figures/unsafe_acceptance_by_corruption.png`
- Rejection figure: `results/figures/rejection_rate_by_corruption.png`
