# MAVS Chapter 10B Phase 6 Verification Report

Generated at UTC: `2026-06-21T18:51:25.436002+00:00`
Requested run mode: `final`
Verification scope: `prepared-checkout artifact integrity and release guard validation`
Overall status: `pass`

## Gate Results

| Check | Status | Summary |
| --- | --- | --- |
| `required_files_exist` | `pass` | 9 required files are present; verification report state is existing. |
| `hashes_match` | `pass` | 520 inventory artifacts were hash-checked. |
| `artifact_inventory_complete` | `pass` | All WorkPlan-required artifact categories are represented. |
| `chapter10a_import_passed` | `pass` | Chapter 10A imported foundation remains validated by the Phase 1 manifest. |
| `no_retraining_performed` | `pass` | No Chapter 10B result directory model-training artifacts or forbidden training commands were detected. |
| `corruption_grid_complete` | `pass` | The corruption grid has the required datasets, corruptions, levels, and independent locked/audit seeds. |
| `stress_matrix_complete` | `pass` | Locked and audit stress matrices are complete and their referenced hashes still match. |
| `anti_overfitting_final_run_guards` | `pass` | Final-run guards are armed; archived exploratory runs are not certified as final runs. |
| `metrics_cover_required_space` | `pass` | Metric rows cover all required datasets, systems, corruption families, and levels for locked and audit splits. |
| `governance_traces_contain_required_fields` | `pass` | Trace indexes contain the required governance fields, schema hashes, and row counts. |
| `reports_reference_existing_artifacts` | `pass` | Report claims and manifest input/output records reference existing artifacts with matching hashes. |
| `path_records_all_phase_evidence` | `pass` | Path.md records the phase trail and console log inventory. |

## Evidence

### required_files_exist

Status: `pass`

```json
{
  "missing": [],
  "verification_report_path": "results/reports/verification_report.md",
  "verification_report_state": "existing"
}
```

### hashes_match

Status: `pass`

```json
{
  "mismatches": [],
  "missing": []
}
```

### artifact_inventory_complete

Status: `pass`

```json
{
  "category_counts": {
    "configs": 15,
    "corruption_manifests": 3,
    "documentation": 5,
    "figures": 186,
    "import_manifests": 6,
    "metric_tables": 16,
    "reports": 6,
    "robustness_curves": 182,
    "scripts": 13,
    "source": 45,
    "stress_run_manifests": 16,
    "tests": 27
  },
  "missing_categories": []
}
```

### chapter10a_import_passed

Status: `pass`

```json
{
  "manifest_path": "results/baseline_import/ch10a_import_manifest.json",
  "manifest_sha256": "d95aa3282c07262162b67bdc462674619ec59f153bea354c4be9223015713e69",
  "source_git_commit": "3f8ce15dac24eaefcd1379279c30f1ded5be9a0b",
  "trace_records_checked": 113828,
  "verification_report_status": "pass"
}
```

### no_retraining_performed

Status: `pass`

```json
{
  "forbidden_manifest_commands": [],
  "generated_model_artifacts": []
}
```

### corruption_grid_complete

Status: `pass`

```json
{
  "corruption_families": [
    "feature_noise",
    "missing_features",
    "random_feature_deletion",
    "label_noise",
    "confidence_distortion",
    "adversarial_confidence_inflation",
    "distribution_shift",
    "synthetic_sensor_failure",
    "specialist_failure"
  ],
  "datasets": [
    "breast_cancer_wisconsin",
    "adult_income",
    "credit_card_fraud",
    "bank_marketing"
  ],
  "definition_count": 2880,
  "grid_manifest_sha256": "bb6e1be969403fb9f7b70c3f88c3949d373af9882ddfa93462221cb5e1d07c87",
  "levels": [
    0.0,
    0.05,
    0.1,
    0.2,
    0.4,
    0.6,
    0.8,
    1.0
  ],
  "seed_overlap": []
}
```

### stress_matrix_complete

Status: `pass`

```json
{
  "failures": [],
  "runs": {
    "audit": {
      "checks": {
        "aggregate_index_hash_matches": true,
        "aggregate_row_count": true,
        "config_hash_matches": true,
        "grid_hash_matches": true,
        "import_hash_matches": true,
        "prediction_index_hash_matches": true,
        "run_status": true,
        "system_run_count": true,
        "trace_artifact_count": true,
        "trace_index_hash_matches": true
      },
      "config_hash_actual": "a0dbc1788c3d736689ffef3822766137c07d45ba6288a97347aebf1a59b13fcd",
      "config_hash_expected": "a0dbc1788c3d736689ffef3822766137c07d45ba6288a97347aebf1a59b13fcd",
      "governance_trace_artifact_count": 2880,
      "run_id": "phase3_audit_full_v1",
      "run_mode": "exploratory",
      "system_run_count": 7200
    },
    "locked": {
      "checks": {
        "aggregate_index_hash_matches": true,
        "aggregate_row_count": true,
        "config_hash_matches": true,
        "grid_hash_matches": true,
        "import_hash_matches": true,
        "prediction_index_hash_matches": true,
        "run_status": true,
        "system_run_count": true,
        "trace_artifact_count": true,
        "trace_index_hash_matches": true
      },
      "config_hash_actual": "6f73e87efb668065a463cef74bcc9c9504bb71ba23eef21a7494c96b58771bcc",
      "config_hash_expected": "6f73e87efb668065a463cef74bcc9c9504bb71ba23eef21a7494c96b58771bcc",
      "governance_trace_artifact_count": 2880,
      "run_id": "phase3_locked_full_v1",
      "run_mode": "exploratory",
      "system_run_count": 7200
    }
  }
}
```

### anti_overfitting_final_run_guards

Status: `pass`

```json
{
  "current_run_modes": [
    "exploratory"
  ],
  "exploratory_final_violations": [],
  "final_config_hash_changes": [],
  "import_hash_changes": [],
  "seed_overlap": [],
  "training_artifacts": []
}
```

### metrics_cover_required_space

Status: `pass`

```json
{
  "failures": [],
  "splits": {
    "audit": {
      "datasets": [
        "adult_income",
        "bank_marketing",
        "breast_cancer_wisconsin",
        "credit_card_fraud"
      ],
      "families": [
        "adversarial_confidence_inflation",
        "confidence_distortion",
        "distribution_shift",
        "feature_noise",
        "label_noise",
        "missing_features",
        "random_feature_deletion",
        "specialist_failure",
        "synthetic_sensor_failure"
      ],
      "levels": [
        "0.0",
        "0.05",
        "0.1",
        "0.2",
        "0.4",
        "0.6",
        "0.8",
        "1.0"
      ],
      "metric_rows_sha256": "a8466327b36897270708bb8cf032cb5c3c3e69ea626dae0c81efb852031b1342",
      "rows": 7200,
      "systems": [
        "mean_ensemble",
        "pure_mavs_gc",
        "single_model",
        "static_weighted_ensemble",
        "veto_mavs"
      ]
    },
    "locked": {
      "datasets": [
        "adult_income",
        "bank_marketing",
        "breast_cancer_wisconsin",
        "credit_card_fraud"
      ],
      "families": [
        "adversarial_confidence_inflation",
        "confidence_distortion",
        "distribution_shift",
        "feature_noise",
        "label_noise",
        "missing_features",
        "random_feature_deletion",
        "specialist_failure",
        "synthetic_sensor_failure"
      ],
      "levels": [
        "0.0",
        "0.05",
        "0.1",
        "0.2",
        "0.4",
        "0.6",
        "0.8",
        "1.0"
      ],
      "metric_rows_sha256": "c6e1b8a598ddf4d84f7f8b23287b91d9568d41ae025d9226ed18ff36e86b0e26",
      "rows": 7200,
      "systems": [
        "mean_ensemble",
        "pure_mavs_gc",
        "single_model",
        "static_weighted_ensemble",
        "veto_mavs"
      ]
    }
  }
}
```

### governance_traces_contain_required_fields

Status: `pass`

```json
{
  "failures": [],
  "splits": {
    "audit": {
      "missing_fields": [],
      "run_id": "phase3_audit_full_v1",
      "sample_invalid_rows": [],
      "trace_index_sha256": "f9a4aac2bf81661f157648c7e4100311d2b3b3f325a67e6a5c7be80ad3aac2cd",
      "trace_rows": 2880
    },
    "locked": {
      "missing_fields": [],
      "run_id": "phase3_locked_full_v1",
      "sample_invalid_rows": [],
      "trace_index_sha256": "9565b0e6f9164ac2c9262b5f0d61d7495b53e2f3c2575c95c777a194b81acef0",
      "trace_rows": 2880
    }
  }
}
```

### reports_reference_existing_artifacts

Status: `pass`

```json
{
  "checked_artifacts": 43,
  "failures": []
}
```

### path_records_all_phase_evidence

Status: `pass`

```json
{
  "console_log_mentions": 343,
  "missing_phase_markers": []
}
```
