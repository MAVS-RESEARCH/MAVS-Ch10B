# MAVS Chapter 10B Path

This file is the implementation trail for `WorkPlan.md`. It must move with the code. Every material implementation step must record what changed, what was verified, and whether the work still follows the plan.

## Source Review Log

Date: 2026-06-20 21:51:59 +05:00

Reviewed supplied documents:

- `C:\Users\Saif malik\Downloads\MAVS Chapter 10B.pdf`
  - 3 pages extracted.
  - Controlling Chapter 10B scope.
  - Mission: determine whether MAVS-GC fails more safely under adverse conditions.
  - Repository named by the document: `mavs-ch10-robustness-benchmarks`.
  - Requires importing trained specialists, MAVS-GC, and baselines from Chapter 10A with no retraining.
  - Requires corruption families: Feature Noise, Missing Features, Label Noise, Confidence Distortion, Distribution Shift, Specialist Failure.
  - Requires every corruption to be parameterized, with example `noise_level = 0.0 -> 1.0`.
  - Requires stress testing Mean Ensemble, Weighted Ensemble, Veto MAVS, and Pure MAVS-GC.
  - Requires metrics: Accuracy Under Corruption, Unsafe Acceptance Rate, Failure Rate, Rejection Rate, Governance Severity, Threshold Distribution.
  - Requires `robustness_curves/`, a robustness benchmark suite, Robustness Report, Corruption Atlas, and Failure Map.

- `C:\Users\Saif malik\Downloads\Mavs.pdf`
  - 5 pages extracted.
  - Defines MAVS as governance-first, not routing, bagging, stacking, or ordinary averaging.
  - Requires all specialists to evaluate every input.
  - Requires governed consensus with specialist scores, supports, diagnostics, severity, weights, mitigation, threshold, decision, and explanation trace.
  - Requires monotone safety behavior, hard veto behavior, bounded mitigation, and deterministic traceability.

- `C:\Users\Saif malik\Downloads\Mavs Research Bible - Chapter 10.pdf`
  - 10 pages extracted.
  - Defines Chapter 10 as the real benchmark layer following Chapter 9 synthetic validation.
  - Confirms Chapter 10B is the Robustness Program.
  - Adds complete evidence requirements: reproducible, statistically supported, multiple datasets, multiple baselines, traces, and reports.
  - Adds shared comparison systems: Single Best Model, Mean Ensemble, Static Weighted Ensemble, Veto MAVS, and Pure MAVS-GC.
  - Adds Chapter 10B corruption families omitted from the shorter Chapter 10B PDF: Random Feature Deletion, Adversarial Confidence Inflation, and Synthetic Sensor Failure.
  - Adds Chapter 10B metrics omitted from the shorter Chapter 10B PDF: F1 Under Corruption, Robustness Curve Area, Governance Severity Distribution, and Governance Threshold Distribution.

- `C:\Users\Saif malik\Downloads\MAVS Research Bible - Chapter 10A Completion Report.pdf`
  - 8 pages extracted.
  - Confirms Chapter 10A Accuracy Benchmark Program is complete.
  - Confirms Chapter 10A evaluated Breast Cancer Wisconsin, Adult Income, Credit Card Fraud, and Bank Marketing.
  - Confirms Chapter 10A evaluated Single Model, Mean Ensemble, Static Weighted Ensemble, Veto MAVS, and Pure MAVS-GC.
  - Confirms Chapter 10A evidence did not support universal predictive-correctness superiority for MAVS-GC.
  - Important Chapter 10B implication: robustness should be tested as risk reduction, error shaping, safety control, calibration behavior, distribution shift behavior, and adversarial resistance rather than assuming direct accuracy improvement.

Extraction method:

- Used the bundled Python runtime with `pdfplumber`.
- Used Poppler `pdfinfo.exe` to verify page counts after locating the Windows Poppler binary.
- Temporary extraction files were created under `tmp/pdfs/` for review.
- Temporary reference clone was created under `tmp/MAVS-Chapter-10A/` for inspection.
- Temporary files are not part of the repository deliverable.

## Current Repository State

Date: 2026-06-20 21:51:59 +05:00

- Target repository from user: `https://github.com/MAVS-RESEARCH/MAVS-Ch10B`
- Local workspace: `C:\Users\Saif malik\MAVS-Ch10B`
- Initial local folder was empty and not a Git repository.
- Repository was cloned into the workspace.
- Initial repository content after clone:
  - `LICENSE`
- No Chapter 10B benchmark implementation existed before this documentation step.

## Chapter 10A Reference Inspection

Date: 2026-06-20 21:51:59 +05:00

Reference repositories and paths inspected:

- GitHub reference requested by user: `https://github.com/MAVS-RESEARCH/MAVS-Chapter-10A`
- Temporary clone for source inspection: `C:\Users\Saif malik\MAVS-Ch10B\tmp\MAVS-Chapter-10A`
- Local completed artifact repository detected: `C:\Users\Saif malik\MAVS-Ch10A`

Observed Chapter 10A source structure:

- `configs/datasets/`
- `configs/models/`
- `configs/systems/`
- `configs/experiments/`
- `src/mavs_ch10a/`
- `scripts/`
- `tests/`
- `results/reports/`

Important Chapter 10A files inspected:

- `README.md`
- `WorkPlan.md`
- `Path.md`
- `pyproject.toml`
- `src/mavs_ch10a/systems/base.py`
- `src/mavs_ch10a/governance/trace.py`
- `scripts/freeze_systems.py`
- `results/reports/reproducibility_manifest.json`
- `results/reports/artifact_inventory.json`
- `results/reports/verification_report.md`

Important Chapter 10A findings:

- The public Chapter 10A repository tracks source, configs, tests, final reports, final figures, reproducibility manifest, artifact inventory, and verification report.
- Heavy generated artifacts are intentionally ignored by git, including raw datasets, processed datasets, checkpoints, full metrics, predictions, and traces.
- Therefore Chapter 10B cannot execute from the GitHub source clone alone. Phase 1 must validate or acquire a Chapter 10A artifact bundle matching the Chapter 10A artifact inventory.
- The local path `C:\Users\Saif malik\MAVS-Ch10A` exists and contains checkpoint files under `results/checkpoints/`, so it is the likely local artifact source for Phase 1.
- The Chapter 10A verification report states overall status `pass`.
- The Chapter 10A verification report records final locked run id `locked_20260620T122552Z` and final audit run id `audit_20260620T122649Z`.
- The Chapter 10A verification report records no final verification failures.

Chapter 10A import implications for Chapter 10B:

- Import must be manifest-driven and hash-checked.
- Import must include source code compatibility plus generated artifact availability.
- Import must not silently recreate or retrain missing artifacts.
- Clean baseline replay must happen before corruption stress testing.

## Work Implemented So Far

### Documentation Bootstrap

Date: 2026-06-20 21:51:59 +05:00

Files created:

- `WorkPlan.md`
- `Path.md`

Code produced:

- No benchmark code has been produced yet.
- This step created the planning and implementation-tracking documents required before code execution.

Commands and actions:

- Loaded the PDF workflow instructions.
- Loaded workspace dependency paths.
- Cloned `MAVS-RESEARCH/MAVS-Ch10B` into the local workspace.
- Verified the initial Chapter 10B repo contained only `LICENSE`.
- Extracted all four supplied PDFs with the bundled Python runtime and `pdfplumber`.
- Verified page counts with Poppler after locating the Windows executable path.
- Cloned `MAVS-RESEARCH/MAVS-Chapter-10A` into a temporary local reference directory for structure inspection.
- Checked for a local completed Chapter 10A artifact repository at `C:\Users\Saif malik\MAVS-Ch10A`.
- Created `WorkPlan.md` and `Path.md`.

Datasets touched:

- None by Chapter 10B code.
- Chapter 10A datasets were inspected only through manifests and repository structure:
  - `breast_cancer_wisconsin`
  - `adult_income`
  - `credit_card_fraud`
  - `bank_marketing`

Models imported, trained, or evaluated:

- None by Chapter 10B code.
- Chapter 10A checkpoint presence was sampled in the local completed artifact repository.
- No model training was run.
- No model evaluation was run.

Corruption families touched:

- None implemented yet.
- Required corruption families were enumerated in `WorkPlan.md`.

Benchmark/test outputs:

- PDF extraction verified:
  - Chapter 10B PDF: 3 pages.
  - MAVS definition PDF: 5 pages.
  - Chapter 10 research bible PDF: 10 pages.
  - Chapter 10A completion report PDF: 8 pages.
- Chapter 10A reference verification report inspected:
  - Overall status: `pass`.
  - Required benchmark matrix: pass.
  - Governance trace schema: pass.
  - Final benchmark run mode and frozen configs: pass.

Artifact hashes:

- No Chapter 10B artifacts generated yet beyond these two markdown files.
- Chapter 10A artifact hashes were inspected in the Chapter 10A manifests but not imported into Chapter 10B yet.

WorkPlan compliance:

- Follows the user's instruction to create both required markdown files from the supplied documents.
- Uses the Chapter 10B document as the controlling implementation scope.
- Uses the Chapter 10 research bible to prevent omissions in corruption families, systems, metrics, and evidence requirements.
- Uses the MAVS definition to define governance trace and safety behavior requirements.
- Uses the Chapter 10A completion report to constrain the import/no-retraining policy and robustness interpretation.

Deviations:

- None.

Risks or limitations:

- The GitHub Chapter 10A source clone does not contain the large generated artifacts needed to execute Chapter 10B. Phase 1 must use a valid local or downloaded Chapter 10A artifact bundle.
- Chapter 10B implementation has not started; only the execution contract and tracking file exist.

Next required action:

- Begin Phase 1 from `WorkPlan.md`: Baseline Import and Frozen Foundation.

### Phase 1 - Baseline Import and Frozen Foundation Implementation

Date: 2026-06-20 22:28:03 +05:00

Files created or changed:

- `.gitignore`
- `README.md`
- `pyproject.toml`
- `configs/ch10a_import/source.yaml`
- `configs/experiments/ch10b_robustness.yaml`
- `external/ch10a/.gitkeep`
- `results/baseline_import/.gitkeep`
- `src/mavs_ch10b/__init__.py`
- `src/mavs_ch10b/cli.py`
- `src/mavs_ch10b/adapters/__init__.py`
- `src/mavs_ch10b/adapters/ch10a_source.py`
- `src/mavs_ch10b/adapters/ch10a_artifacts.py`
- `src/mavs_ch10b/adapters/ch10a_systems.py`
- `src/mavs_ch10b/adapters/baseline_runner.py`
- `src/mavs_ch10b/verification/hash_utils.py`
- `src/mavs_ch10b/verification/import_audit.py`
- `scripts/import_ch10a_foundation.py`
- `scripts/run_clean_baseline.py`
- `tests/test_ch10a_import_contract.py`
- `tests/test_no_retraining_guard.py`
- `tests/test_clean_baseline_replay.py`
- `tests/test_trace_schema_compatibility.py`
- `results/baseline_import/ch10a_import_manifest.json`
- `results/baseline_import/ch10a_import_report.md`
- `results/baseline_import/clean_replay_metrics.csv`
- `results/baseline_import/clean_replay_comparison.csv`
- `results/baseline_import/clean_replay_manifest.json`
- `results/baseline_import/clean_replay_compatibility_report.md`
- `Path.md`

Code produced:

- Python package metadata and CLI entry point through `pyproject.toml`.
- Chapter 10A source locator in `src/mavs_ch10b/adapters/ch10a_source.py`:
  - reads `configs/ch10a_import/source.yaml`,
  - supports `MAVS_CH10A_ROOT`,
  - supports configured absolute local artifact path,
  - supports fallback candidate paths,
  - validates the selected path is a Chapter 10A repository with generated reports.
- Chapter 10A artifact validator in `src/mavs_ch10b/adapters/ch10a_artifacts.py`:
  - verifies Chapter 10A reproducibility manifest, artifact inventory, verification report, frozen system manifest, dataset manifests, benchmark splits, specialist checkpoints, checkpoint metadata, system configs, benchmark summaries, and run manifests,
  - checks the Chapter 10A verification report status,
  - validates all Chapter 10A artifact inventory hashes,
  - validates governance trace schema fields for Veto MAVS and Pure MAVS-GC traces,
  - collects config, checkpoint, and benchmark split hashes for the Chapter 10B import manifest.
- Chapter 10A system adapter in `src/mavs_ch10b/adapters/ch10a_systems.py`:
  - registers the Chapter 10A `src` path without copying source files,
  - loads the frozen Phase 3 system manifest,
  - loads specialist-output bundles from Chapter 10A,
  - builds all five frozen comparison systems from the Chapter 10A manifest,
  - wraps system execution outputs in a Chapter 10B `SystemRunBundle`.
- Clean baseline replay runner in `src/mavs_ch10b/adapters/baseline_runner.py`:
  - executes every imported system on clean `locked_benchmark` and `audit_benchmark` splits,
  - computes the Chapter 10A metric set through the Chapter 10A metric function,
  - compares replayed metrics against Chapter 10A clean metric summaries at tolerance `1e-12`,
  - writes clean replay metrics, comparison table, compatibility report, and manifest.
- Verification utilities in `src/mavs_ch10b/verification/hash_utils.py` and `src/mavs_ch10b/verification/import_audit.py`:
  - SHA-256 hashing for files and canonical JSON,
  - JSON artifact persistence,
  - git commit capture,
  - dependency version capture,
  - no-training command guard,
  - import manifest and import report generation.
- Script wrappers:
  - `scripts/import_ch10a_foundation.py`
  - `scripts/run_clean_baseline.py`
- Tests:
  - Chapter 10A import contract validation,
  - no-retraining guard,
  - clean replay artifact and matrix validation,
  - governance trace schema sample compatibility.

Commands run:

- `python scripts\import_ch10a_foundation.py`
  - Result: success.
  - Validated `C:\Users\Saif malik\MAVS-Ch10A` as the Chapter 10A artifact source.
  - Required files checked: `50`.
  - Missing required files: `0`.
  - Artifact inventory artifacts checked: `357`.
  - Artifact inventory missing: `0`.
  - Artifact inventory mismatches: `0`.
  - Governance trace records checked: `113828`.
  - Governance trace schema failures: `0`.
  - Chapter 10A verification report status: `pass`.
- `python scripts\run_clean_baseline.py`
  - Result: success.
  - Executed all `4` datasets, `2` benchmark splits, and `5` systems.
  - Clean replay metric rows: `40`.
  - Clean replay metric comparison rows: `360`.
  - Clean replay comparison failures: `0`.
  - Tolerance: `1e-12`.
- `python -m pytest -q`
  - Result: `5 passed`.
  - Warning: pytest could not create `.pytest_cache` because of a Windows access-denied cache path issue. This did not affect test execution.
- `python -m pytest -q -p no:cacheprovider`
  - Result: `5 passed`.
- Console instrumentation audit:
  - Result: `CONSOLE_COMMENT_CHECK PASS`.
  - Phase 1 `console.log(...)` calls checked: `33`.
  - Every `console.log(...)` call has an immediately adjacent `Phase 1 console.log:` comment.
- Phase 1 stress audit:
  - Result: `PHASE1_STRESS_AUDIT PASS`.
  - Failures: `[]`.

Datasets touched:

- No dataset was created, modified, or retrained by Chapter 10B.
- Imported and replayed Chapter 10A clean benchmark splits for:
  - `breast_cancer_wisconsin`
  - `adult_income`
  - `credit_card_fraud`
  - `bank_marketing`

Models imported, trained, or evaluated:

- Imported/evaluated frozen Chapter 10A specialists:
  - `random_forest`
  - `gradient_boosted_trees`
  - `mlp`
- Imported/evaluated frozen Chapter 10A systems:
  - `single_model`
  - `mean_ensemble`
  - `static_weighted_ensemble`
  - `veto_mavs`
  - `pure_mavs_gc`
- No Chapter 10B training command was run.
- No Chapter 10B checkpoint or `.joblib` artifact was created.

Corruption families touched:

- None. Phase 1 establishes the clean imported foundation only.

Benchmark/test outputs:

- Import audit:
  - Chapter 10A source path: `C:\Users\Saif malik\MAVS-Ch10A`
  - Chapter 10A current source git commit: `3f8ce15dac24eaefcd1379279c30f1ded5be9a0b`
  - Chapter 10A manifest git commit: `e713e2f7812a01adc7dde4502453b51e6340725d`
  - Chapter 10A verification report status: `pass`
  - Required files checked: `50`
  - Artifact inventory checked: `357`
  - Governance trace records checked: `113828`
- Clean baseline replay:
  - Metric rows: `40`
  - Comparison rows: `360`
  - Comparison failures: `0`
  - Splits: `locked_benchmark`, `audit_benchmark`
  - Systems per split: `single_model`, `mean_ensemble`, `static_weighted_ensemble`, `veto_mavs`, `pure_mavs_gc`
- Test suite:
  - `5 passed`.
- Stress audit:
  - Matrix coverage passed for `4` datasets, `2` splits, `5` systems, and `9` metrics.
  - Hash checks passed for generated clean replay artifacts.
  - No Chapter 10B `.joblib` artifacts were present.
  - ASCII check passed for created `.py`, `.md`, `.toml`, `.yaml`, and `.yml` text files.

Artifact hashes:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `results/baseline_import/ch10a_import_manifest.json` | 8067 | `d95aa3282c07262162b67bdc462674619ec59f153bea354c4be9223015713e69` |
| `results/baseline_import/ch10a_import_report.md` | 574 | `3b09286d98fc06b4731bd7ab6c89ade991844de470132f5fde69e52d8db00831` |
| `results/baseline_import/clean_replay_metrics.csv` | 10305 | `24710564c34e94e6cb50e5c6806a8c9de3b987bdd36e15c144b57514a6930dea` |
| `results/baseline_import/clean_replay_comparison.csv` | 43614 | `22c16841a143fda79ad59cabb82dfc4bcd5d4fb3ccd1015efcb13d0d1b9ec9e2` |
| `results/baseline_import/clean_replay_manifest.json` | 1756 | `455d71537dc53fa7075256928af57b80bf2ac02a115b53dcae46d3040421835f` |
| `results/baseline_import/clean_replay_compatibility_report.md` | 177 | `e3f48e1c57b27617b61ea719d19972f0214ac2967082a86c38a85b4d73324720` |

Imported Chapter 10A checkpoint hashes:

| Dataset | Random Forest | Gradient Boosted Trees | MLP |
| --- | --- | --- | --- |
| `breast_cancer_wisconsin` | `e763e80483bf169ec6c2c3040bbe9275ad00137ebd58a3921635eb7025465381` | `13b82b2b1487dcc7e99e81ce3b4d2e2a92cfa5ae1c839afe8c77226f2a7cca8a` | `bac8e09215ab98f8928c67ddd71f4e2e4e77b88445bc7b1ae1306d070598bd6b` |
| `adult_income` | `a8b6f44616086ad2bee97c1e4e085742fe2552af7266ee96eaae2258904c0d33` | `fd2d2a94658c09e12359a383b45c21a17376d2a6dc07e9552f829ba91010dbf2` | `59b61679a724cb71db2dcb15041f6e7f57b9c7c86d18494400961f116b2e9730` |
| `credit_card_fraud` | `ccbc38b880650d9257c9e2299822f3c6f1fcbf426db1e1d0082fc0b0522248e4` | `387443a61cd607bd57dc9da44c5216bb56abc8bc656c5f363a69b662c9e052a4` | `95dac92138873572e9d4306f07ba9c78d8bf6196649ab1659794e0a6422ca77b` |
| `bank_marketing` | `1e9317a06ff130a29838351395d08f313a412865de51a19c5d33dd425f7ace5d` | `d5348dc33229586af0089d608f6695a9a71d06ff3a468f1824af279611ac2daf` | `c6ec610946b949be3779ae8c57d13295270ac67ffb2901b82391fff29eb3fc19` |

Imported Chapter 10A benchmark split hashes:

| Dataset | Locked Benchmark | Audit Benchmark |
| --- | --- | --- |
| `breast_cancer_wisconsin` | `df16c6d1115410cbd9ae7ef64c91e7124f7588cd7c3578937be2ce1ea775cb1f` | `9e3b93d165a4acd41ea149560790a789e8d0c2fbe66568e93c77bcdc31cbec10` |
| `adult_income` | `58dd6dc19c7e449bc83add0bbed8fe7f45420c5c725e1bbf1d820a15d2e936b7` | `3f81bddd1fd5b5559559baf44c77600fcc08617091932efc106be3aa1a3ba23d` |
| `credit_card_fraud` | `0ec4001387aab45538cfde6d0fd9be420f0e9bd284199eb23fd2301c3b2d9662` | `ef411e816f4d3865781cde435ab9ee9e5244e226343a9fab818e881e8519e116` |
| `bank_marketing` | `69fb34cb90185d147c25a31e2a669b50bba05dd7bb6507c8c08e8dbc09805cb8` | `60cec716522376107b0917c11861eeae0fcf138b89bbffda16a4b8ade3562a7a` |

Console instrumentation inventory:

- `scripts/run_clean_baseline.py:24` comment: `Phase 1 console.log: records clean baseline script dispatch.`
- `scripts/run_clean_baseline.py:25` code: `console.log("phase1.script.clean_baseline_dispatch", repo_root=str(repo_root), config=str(args.config), tolerance=args.tolerance)`
- `scripts/run_clean_baseline.py:27` comment: `Phase 1 console.log: records clean baseline script completion.`
- `scripts/run_clean_baseline.py:28` code: `console.log("phase1.script.clean_baseline_complete", comparison_failures=manifest["comparison_failures"], metric_rows=manifest["metric_rows"])`
- `scripts/import_ch10a_foundation.py:22` comment: `Phase 1 console.log: records import script dispatch.`
- `scripts/import_ch10a_foundation.py:23` code: `console.log("phase1.script.import_dispatch", repo_root=str(repo_root), config=str(args.config))`
- `scripts/import_ch10a_foundation.py:25` comment: `Phase 1 console.log: records import script completion.`
- `scripts/import_ch10a_foundation.py:26` code: `console.log("phase1.script.import_complete", manifest_path=manifest["report_path"], status=manifest["verification_report_status"])`
- `src/mavs_ch10b/cli.py:31` comment: `Phase 1 console.log: records CLI dispatch for the Chapter 10A foundation import.`
- `src/mavs_ch10b/cli.py:32` code: `console.log("phase1.cli.import_foundation_dispatch", repo_root=str(repo_root), config=str(args.config))`
- `src/mavs_ch10b/cli.py:38` comment: `Phase 1 console.log: records CLI dispatch for the clean baseline replay.`
- `src/mavs_ch10b/cli.py:39` code: `console.log("phase1.cli.clean_baseline_dispatch", repo_root=str(repo_root), config=str(args.config), tolerance=args.tolerance)`
- `src/mavs_ch10b/verification/import_audit.py:28` comment: `Phase 1 console.log: records no-retraining command guard evaluation.`
- `src/mavs_ch10b/verification/import_audit.py:29` code: `console.log("phase1.import_audit.no_training_command_checked", command_line=command_line, forbidden=forbidden)`
- `src/mavs_ch10b/verification/import_audit.py:38` comment: `Phase 1 console.log: records Chapter 10A foundation import audit dispatch.`
- `src/mavs_ch10b/verification/import_audit.py:39` code: `console.log("phase1.import_audit.dispatch", repo_root=str(repo_root), output_dir=str(output_dir), config=str(config_path))`
- `src/mavs_ch10b/verification/import_audit.py:79` comment: `Phase 1 console.log: records Chapter 10A import manifest completion.`
- `src/mavs_ch10b/verification/import_audit.py:80` code: `console.log(...)`
- `src/mavs_ch10b/verification/import_audit.py:116` comment: `Phase 1 console.log: records Chapter 10A import report persistence.`
- `src/mavs_ch10b/verification/import_audit.py:117` code: `console.log("phase1.import_audit.report_written", path=str(path))`
- `src/mavs_ch10b/verification/hash_utils.py:51` comment: `Phase 1 console.log: records JSON artifact persistence.`
- `src/mavs_ch10b/verification/hash_utils.py:52` code: `console.log("phase1.hash_utils.json_written", path=str(path), sha256=hash_file(path))`
- `src/mavs_ch10b/adapters/ch10a_source.py:30` comment: `Phase 1 console.log: records Chapter 10A source configuration loading.`
- `src/mavs_ch10b/adapters/ch10a_source.py:31` code: `console.log("phase1.ch10a_source.config_loaded", path=str(resolved), keys=sorted(config.keys()))`
- `src/mavs_ch10b/adapters/ch10a_source.py:38` comment: `Phase 1 console.log: records Chapter 10A source candidate enumeration.`
- `src/mavs_ch10b/adapters/ch10a_source.py:39` code: `console.log("phase1.ch10a_source.candidates_built", candidates=[str(path) for path in candidates])`
- `src/mavs_ch10b/adapters/ch10a_source.py:47` comment: `Phase 1 console.log: records selected Chapter 10A artifact repository.`
- `src/mavs_ch10b/adapters/ch10a_source.py:48` code: `console.log("phase1.ch10a_source.located", repo_root=str(source.repo_root), source_repo_url=source.source_repo_url)`
- `src/mavs_ch10b/adapters/ch10a_source.py:57` comment: `Phase 1 console.log: records Chapter 10A source import path registration.`
- `src/mavs_ch10b/adapters/ch10a_source.py:58` code: `console.log("phase1.ch10a_source.import_path_ready", src_path=src_path, present=src_path in sys.path)`
- `src/mavs_ch10b/adapters/ch10a_artifacts.py:94` comment: `Phase 1 console.log: records required Chapter 10A file presence validation.`
- `src/mavs_ch10b/adapters/ch10a_artifacts.py:95` code: `console.log("phase1.ch10a_artifacts.required_files_checked", checked=len(required_files), missing=len(missing))`
- `src/mavs_ch10b/adapters/ch10a_artifacts.py:98` comment: `Phase 1 console.log: records Chapter 10A verification report status extraction.`
- `src/mavs_ch10b/adapters/ch10a_artifacts.py:99` code: `console.log("phase1.ch10a_artifacts.verification_report_status", status=verification_status)`
- `src/mavs_ch10b/adapters/ch10a_artifacts.py:110` comment: `Phase 1 console.log: records Chapter 10A artifact inventory hash validation.`
- `src/mavs_ch10b/adapters/ch10a_artifacts.py:111` code: `console.log(...)`
- `src/mavs_ch10b/adapters/ch10a_artifacts.py:124` comment: `Phase 1 console.log: records Chapter 10A governance trace schema validation.`
- `src/mavs_ch10b/adapters/ch10a_artifacts.py:125` code: `console.log("phase1.ch10a_artifacts.trace_schema_checked", checked_records=trace_checked, failures=len(trace_failures))`
- `src/mavs_ch10b/adapters/ch10a_artifacts.py:143` comment: `Phase 1 console.log: records complete Chapter 10A foundation validation result.`
- `src/mavs_ch10b/adapters/ch10a_artifacts.py:144` code: `console.log(...)`
- `src/mavs_ch10b/adapters/ch10a_systems.py:28` comment: `Phase 1 console.log: records Chapter 10A frozen system manifest loading.`
- `src/mavs_ch10b/adapters/ch10a_systems.py:29` code: `console.log("phase1.ch10a_systems.frozen_manifest_loaded", path=str(path), datasets=len(manifest.get("datasets", {})))`
- `src/mavs_ch10b/adapters/ch10a_systems.py:38` comment: `Phase 1 console.log: records Chapter 10A specialist-output bundle loading.`
- `src/mavs_ch10b/adapters/ch10a_systems.py:39` code: `console.log(...)`
- `src/mavs_ch10b/adapters/ch10a_systems.py:70` comment: `Phase 1 console.log: records construction of frozen Chapter 10A comparison systems.`
- `src/mavs_ch10b/adapters/ch10a_systems.py:71` code: `console.log("phase1.ch10a_systems.comparison_systems_built", dataset_id=dataset_id, systems=list(system_ids))`
- `src/mavs_ch10b/adapters/ch10a_systems.py:88` comment: `Phase 1 console.log: records one frozen Chapter 10A system execution.`
- `src/mavs_ch10b/adapters/ch10a_systems.py:89` code: `console.log(...)`
- `src/mavs_ch10b/adapters/baseline_runner.py:36` comment: `Phase 1 console.log: records clean baseline replay dispatch.`
- `src/mavs_ch10b/adapters/baseline_runner.py:37` code: `console.log("phase1.baseline_runner.dispatch", ch10a_root=str(source.repo_root), output_dir=str(output_dir), tolerance=tolerance_value)`
- `src/mavs_ch10b/adapters/baseline_runner.py:42` comment: `Phase 1 console.log: records clean replay split start.`
- `src/mavs_ch10b/adapters/baseline_runner.py:43` code: `console.log("phase1.baseline_runner.split_start", split_label=split_label, split=split_name)`
- `src/mavs_ch10b/adapters/baseline_runner.py:66` comment: `Phase 1 console.log: records clean replay metric computation for one system.`
- `src/mavs_ch10b/adapters/baseline_runner.py:67` code: `console.log(...)`
- `src/mavs_ch10b/adapters/baseline_runner.py:112` comment: `Phase 1 console.log: records clean baseline replay completion.`
- `src/mavs_ch10b/adapters/baseline_runner.py:113` code: `console.log(...)`
- `src/mavs_ch10b/adapters/baseline_runner.py:132` comment: `Phase 1 console.log: records Chapter 10A metric function use during clean replay.`
- `src/mavs_ch10b/adapters/baseline_runner.py:133` code: `console.log("phase1.baseline_runner.ch10a_metrics_computed", rows=metrics["rows"], accuracy=metrics["accuracy"])`
- `src/mavs_ch10b/adapters/baseline_runner.py:166` comment: `Phase 1 console.log: records clean replay compatibility comparison construction.`
- `src/mavs_ch10b/adapters/baseline_runner.py:167` code: `console.log("phase1.baseline_runner.comparison_built", rows=len(comparison_records), tolerance=tolerance)`
- `src/mavs_ch10b/adapters/baseline_runner.py:178` comment: `Phase 1 console.log: records Chapter 10A source metric summary loading.`
- `src/mavs_ch10b/adapters/baseline_runner.py:179` code: `console.log("phase1.baseline_runner.source_metrics_loaded", split_label=split_label, path=str(path))`
- `src/mavs_ch10b/adapters/baseline_runner.py:191` comment: `Phase 1 console.log: records CSV artifact persistence.`
- `src/mavs_ch10b/adapters/baseline_runner.py:192` code: `console.log("phase1.baseline_runner.csv_written", path=str(path), rows=len(records))`
- `src/mavs_ch10b/adapters/baseline_runner.py:214` comment: `Phase 1 console.log: records clean replay compatibility report persistence.`
- `src/mavs_ch10b/adapters/baseline_runner.py:215` code: `console.log("phase1.baseline_runner.compatibility_report_written", path=str(path), failures=len(failures))`

WorkPlan compliance:

- Satisfies Phase 1 source/artifact location requirement by locating `C:\Users\Saif malik\MAVS-Ch10A`.
- Satisfies required artifact validation:
  - checkpoints present,
  - processed locked and audit splits present,
  - system configs present,
  - manifests present,
  - Chapter 10A verification report present and passing.
- Satisfies clean baseline replay requirement across all four datasets, two benchmark splits, and five systems.
- Satisfies clean replay compatibility requirement with `360` metric comparisons and `0` failures.
- Satisfies no-retraining requirement:
  - no training command was run,
  - no Chapter 10B checkpoint artifacts were created,
  - frozen Chapter 10A system manifest was used for single-model choices and static weights.
- Satisfies Path.md documentation requirement for commands, artifacts, hashes, line references, and deviations.

Deviations:

- None from Phase 1 intent or acceptance criteria.

Risks or limitations:

- Clean replay used the current local Python environment with `sklearn 1.7.1` while imported Chapter 10A checkpoints were created under `sklearn 1.9.0`. The replay emitted scikit-learn `InconsistentVersionWarning` messages. This is a runtime compatibility risk, but the clean replay reproduced all Chapter 10A metrics exactly within `1e-12`, and Chapter 10A already contains a narrow compatibility shim for the observed calibration checkpoint path.
- The Chapter 10A current source git commit is `3f8ce15dac24eaefcd1379279c30f1ded5be9a0b`, while the Chapter 10A reproducibility manifest records benchmark artifact git commit `e713e2f7812a01adc7dde4502453b51e6340725d`. This was recorded as provenance, not treated as a failure, because artifact hashes, verification status, and clean replay compatibility passed.
- Phase 1 depends on the local completed Chapter 10A artifact repository at `C:\Users\Saif malik\MAVS-Ch10A`. A clean machine must provide an equivalent artifact bundle matching the imported hashes.

Next required action:

- Begin Phase 2 from `WorkPlan.md`: Parameterized Corruption Engine.

### Phase 2 - Parameterized Corruption Engine

Date:

- 2026-06-20 23:11:11 +05:00

Files created or changed:

- Corruption configs:
  - `configs/corruptions/feature_noise.yaml`
  - `configs/corruptions/missing_features.yaml`
  - `configs/corruptions/random_feature_deletion.yaml`
  - `configs/corruptions/label_noise.yaml`
  - `configs/corruptions/confidence_distortion.yaml`
  - `configs/corruptions/adversarial_confidence_inflation.yaml`
  - `configs/corruptions/distribution_shift.yaml`
  - `configs/corruptions/synthetic_sensor_failure.yaml`
  - `configs/corruptions/specialist_failure.yaml`
  - `configs/corruptions/corruption_grid.yaml`
- Corruption engine source:
  - `src/mavs_ch10b/corruptions/__init__.py`
  - `src/mavs_ch10b/corruptions/base.py`
  - `src/mavs_ch10b/corruptions/feature_noise.py`
  - `src/mavs_ch10b/corruptions/missing_features.py`
  - `src/mavs_ch10b/corruptions/random_feature_deletion.py`
  - `src/mavs_ch10b/corruptions/label_noise.py`
  - `src/mavs_ch10b/corruptions/confidence_distortion.py`
  - `src/mavs_ch10b/corruptions/adversarial_confidence_inflation.py`
  - `src/mavs_ch10b/corruptions/distribution_shift.py`
  - `src/mavs_ch10b/corruptions/synthetic_sensor_failure.py`
  - `src/mavs_ch10b/corruptions/specialist_failure.py`
  - `src/mavs_ch10b/corruptions/registry.py`
  - `src/mavs_ch10b/corruptions/grid.py`
  - `src/mavs_ch10b/corruptions/manifest.py`
- Script and result placeholders:
  - `scripts/build_corruption_grid.py`
  - `results/corruption_manifests/.gitkeep`
  - `.gitignore`
- Tests:
  - `tests/__init__.py`
  - `tests/test_corruption_parameterization.py`
  - `tests/test_corruption_determinism.py`
  - `tests/test_corruption_label_cleanliness.py`
  - `tests/test_corruption_bounds.py`
  - `tests/test_corruption_manifest_schema.py`

Code produced:

- Added a common `Corruption` interface in `src/mavs_ch10b/corruptions/base.py`.
  - `CorruptionInput` stores dataset id, split, row ids, feature names, specialist ids, processed features, clean labels, probabilities, and supports.
  - `CorruptionRunDefinition` stores dataset id, split label, split, family, level, seed, seed role, target space, config hash, and immutable corruption id.
  - `CorruptionOutput` stores row ids, features, `y_clean`, `y_observed`, probabilities, supports, masks, failed specialists, distribution-shift metadata, and family metadata.
  - `Corruption.apply(...)` validates `level in [0, 1]`, validates input and output bundle shapes, emits start and completion logs, and returns a copied output bundle.
  - `Corruption.manifest(...)` records input bundle hash, output bundle hash, feature mask hash, clean score hash, corrupted score hash, clean label hash, observed label hash, failed specialist list, distribution descriptor, config hash, seed hash, and applied manifest hash.
  - `deterministic_rng(...)` derives the numpy random generator seed from dataset id, split, family, level, seed, and seed role.
- Added nine required corruption families.
  - Feature Noise: feature-space additive Gaussian noise scaled by column standard deviation and `max_std_multiplier`.
  - Missing Features: feature-space cell-level masking to a deterministic fill value.
  - Random Feature Deletion: feature-space column-level masking to a deterministic fill value.
  - Label Noise: label-space `y_observed` flips while preserving `y_clean`.
  - Confidence Distortion: score-space probability compression toward uncertainty with valid probability and support bounds.
  - Adversarial Confidence Inflation: label-aware score-space inflation or deflation of eligible wrong specialist probabilities, disclosed in metadata with `label_aware: true`.
  - Distribution Shift: deterministic row subset selection by feature norm while preserving row ids and clean labels for selected rows.
  - Synthetic Sensor Failure: deterministic contiguous feature-group masking with affected group metadata.
  - Specialist Failure: score-space specialist channel replacement with constant uncertainty while keeping failed specialist ids represented in metadata.
- Added a required-family registry in `src/mavs_ch10b/corruptions/registry.py`.
  - The registry loads all corruption config files.
  - It fails if any required family is absent or if a config declares the wrong family.
  - The family order is fixed as `feature_noise`, `missing_features`, `random_feature_deletion`, `label_noise`, `confidence_distortion`, `adversarial_confidence_inflation`, `distribution_shift`, `synthetic_sensor_failure`, `specialist_failure`.
- Added the grid builder in `src/mavs_ch10b/corruptions/grid.py`.
  - It expands dataset, split, family, level, seed role, and seed into immutable corruption run definitions.
  - It writes one per-run definition manifest per grid row under `results/corruption_manifests/manifests/`.
  - It writes `corruption_manifest_index.csv`, `corruption_manifest_index.json`, and `corruption_grid_manifest.json`.
  - It hashes every per-run manifest and stores the hash in the index.
- Added the applied manifest schema helper in `src/mavs_ch10b/corruptions/manifest.py`.
  - It validates required applied manifest fields.
  - It persists applied manifest payloads when later benchmark runners call it.
- Added `scripts/build_corruption_grid.py`.
  - It dispatches the grid build and manifest write through the package code.

Grid choices and seed protocol:

- Datasets:
  - `breast_cancer_wisconsin`
  - `adult_income`
  - `credit_card_fraud`
  - `bank_marketing`
- Splits:
  - `locked`: `locked_benchmark`
  - `audit`: `audit_benchmark`
- Corruption families:
  - `feature_noise`
  - `missing_features`
  - `random_feature_deletion`
  - `label_noise`
  - `confidence_distortion`
  - `adversarial_confidence_inflation`
  - `distribution_shift`
  - `synthetic_sensor_failure`
  - `specialist_failure`
- Levels:
  - `0.0`, `0.05`, `0.10`, `0.20`, `0.40`, `0.60`, `0.80`, `1.0`
- Seeds:
  - Locked primary seeds: `1001`, `1002`, `1003`
  - Audit seeds: `2001`, `2002`, `2003`
  - Shadow verification seeds: `9001`, `9002`
- Grid size:
  - `4 datasets * 2 splits * 9 families * 8 levels * 5 seeds per split = 2880 run definitions`
  - Locked primary definitions: `864`
  - Locked shadow definitions: `576`
  - Audit definitions: `864`
  - Audit shadow definitions: `576`
- Seed independence:
  - Locked primary seeds and audit seeds are disjoint.
  - Shadow verification seeds are disjoint from locked primary and audit seeds.
  - Shadow seeds are recorded for reproducibility checks only and are not tuning seeds.

Commands run:

- Regenerated the corruption definition grid:
  - `$env:PYTHONPATH='src'; python scripts\build_corruption_grid.py`
  - Result: `2880` definitions written.
- Full automated test suite:
  - `$env:PYTHONPATH='src'; python -m pytest -q -p no:cacheprovider`
  - Result: `14 passed in 0.61s`.
- Independent stress audit:
  - Verified manifest counts, index counts, per-run manifest hashes, split-role counts, seed separation, level-zero clean behavior, level-one bounds, label cleanliness, row traceability, applied manifest schema, Chapter 10A hash immutability, absence of Ch10B `.joblib` artifacts, console log comment coverage, and ASCII-only Phase 2 source/config files.
  - Result: `STRESS_AUDIT PASS`.

Datasets touched:

- No dataset file was modified.
- The grid references the four frozen Chapter 10A dataset ids:
  - `breast_cancer_wisconsin`
  - `adult_income`
  - `credit_card_fraud`
  - `bank_marketing`
- Phase 2 tests used synthetic in-memory bundles only for corruption behavior tests.

Models imported, trained, or evaluated:

- No model was trained.
- No model checkpoint was created in Chapter 10B.
- No `.joblib` model artifact exists under `results/` after Phase 2.
- The stress audit recomputed Chapter 10A artifact inventory, reproducibility manifest, verification report, checkpoint hashes, system config hashes, and split hashes against the Phase 1 import manifest.
- Chapter 10A hashes remained unchanged.

Corruption families touched:

- All nine required families were implemented and registered.
- All nine families support `level=0.0` and `level=1.0`.
- Stochastic families use deterministic seeds derived from dataset id, split, family, level, seed, and seed role.
- Non-label corruptions preserve `y_clean` and `y_observed`.
- `label_noise` preserves `y_clean` and changes only `y_observed`.
- `distribution_shift` preserves row-id traceability and compares labels by selected row ids because the output row set can be smaller than the input row set.

Benchmark/test outputs:

- `python -m pytest -q -p no:cacheprovider`
  - `14 passed in 0.61s`
- Stress audit output:
  - `STRESS_AUDIT PASS`
  - `definitions 2880`
  - `index_rows 2880`
  - `per_run_manifests 2880`
  - `families 9`
  - `levels [0.0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]`
  - `split_role_counts {('locked', 'primary'): 864, ('locked', 'shadow'): 576, ('audit', 'audit'): 864, ('audit', 'shadow'): 576}`
  - `console_log_calls 47`
  - `phase2_console_log_comments 14`
  - `input_bundle_hash 6d01a21fe9e1ca8f9c1d4888c683147f959b9f25008510aac67fd6944b08dd23`

Artifact hashes:

- Generated Phase 2 artifacts:
  - `results/corruption_manifests/corruption_grid_manifest.json`: `bb6e1be969403fb9f7b70c3f88c3949d373af9882ddfa93462221cb5e1d07c87`
  - `results/corruption_manifests/corruption_manifest_index.csv`: `66b2e473e2fe2413f2dda9ad9d23d58add5e9e56c36ea9d5284053342cd1f09c`
  - `results/corruption_manifests/corruption_manifest_index.json`: `4444e5ed3066fb7d18bcac1de4739f5c4108ec57c3b253a109745d3a4e262803`
  - Per-run manifest count under `results/corruption_manifests/manifests/`: `2880`
  - Every per-run manifest file hash matched the hash recorded in `corruption_manifest_index.csv`.
- Config file hashes:
  - `configs/corruptions/feature_noise.yaml`: `afbad1d4fd801dd833e54f33aaf104ce5c75c2e4fabd012ed5320372f9c2bfa5`
  - `configs/corruptions/missing_features.yaml`: `b9b089e0eb399c7b9112d0595d9be5492efc08ac13325f990f995a246d8c3022`
  - `configs/corruptions/random_feature_deletion.yaml`: `3d34b5163edbc1e635d9704f943f85141e5986255f76d17aa1fc9ff084a2788d`
  - `configs/corruptions/label_noise.yaml`: `289c3cb6dfd1e2cba00ff44fefef5f410f8d5b97793726b5728ffa066dc2dfe0`
  - `configs/corruptions/confidence_distortion.yaml`: `d7ff39d9b9a0d3f263508c1f242ea6d31a654001bc6e3fe8ba5e66e06343bf32`
  - `configs/corruptions/adversarial_confidence_inflation.yaml`: `1d24d7492d568163431d0eef70ed54f368f48eea70aa36e3d76c2e33740b6528`
  - `configs/corruptions/distribution_shift.yaml`: `cb5d9d60cc04acfcce0cb03a5a4c19680464e5e66bd3e59c51859066c24b4d3d`
  - `configs/corruptions/synthetic_sensor_failure.yaml`: `5bbe8e7a7cd5f5d89fcc7b91aa8c222f9746b5f689b30e0710cf86bb4549e0f0`
  - `configs/corruptions/specialist_failure.yaml`: `8cf8dcf98116c9645779379597beea962fb3de6ef47e18cb5b952ee72b42f7be`
  - `configs/corruptions/corruption_grid.yaml`: `2128571460510471a818eefdcce637cdda699a5a1da49e3922686f8dd0532356`
- Source and test file hashes:
  - `src/mavs_ch10b/corruptions/base.py`: `c104fe824ee7fa803f71df386d35a3f8a0ef22227d4ce9ce142e509dde774c14`
  - `src/mavs_ch10b/corruptions/feature_noise.py`: `ae900b27cd49db045ad121a473f571ca03d7bca7917a2b9e3076789088a0538e`
  - `src/mavs_ch10b/corruptions/missing_features.py`: `b6d52e7fcd9d1f3dfb360c31cdfa7db6df5090ef631b90df8d2b4c15551111e1`
  - `src/mavs_ch10b/corruptions/random_feature_deletion.py`: `23a148e9bfeded042f02899d3dd5f183993ddd80a602414e26b18ab48b89e228`
  - `src/mavs_ch10b/corruptions/label_noise.py`: `46477fd7753c47241ae1afb05535a863e894c3aff7777461e27232e80c1438cc`
  - `src/mavs_ch10b/corruptions/confidence_distortion.py`: `025412c17e77faf0235966ad91304063353aa80113c7d7303992153904785c38`
  - `src/mavs_ch10b/corruptions/adversarial_confidence_inflation.py`: `1ea3b1e6fb8171e7cd00d5b0a3c0a12d105057b16aef4e41960ac25d5fa7798e`
  - `src/mavs_ch10b/corruptions/distribution_shift.py`: `3d29d06a1674ba95683a4c8005db107e9b279bfbee4e982e9f93f57b97c885e6`
  - `src/mavs_ch10b/corruptions/synthetic_sensor_failure.py`: `8c593f1a89d161d1e988f4cc9d479a1547da6b8608785e889cef97eb8592621b`
  - `src/mavs_ch10b/corruptions/specialist_failure.py`: `f7aa325736ba3f3df044c5f3d9b7e9d49baafee3123714bfdced4dd894072fd4`
  - `src/mavs_ch10b/corruptions/registry.py`: `a82399b067b5bb8600e864ee0bc48b74966971db29ef393d3ac9a648b166b841`
  - `src/mavs_ch10b/corruptions/grid.py`: `e57a0f31ad6b425fd94b1b600db519101b2e3949dc57c00b3024e23e2f59db7c`
  - `src/mavs_ch10b/corruptions/manifest.py`: `1d4345798f9fcde7e2ca1db0a86fecefc0b530641934687c92da242207259c02`
  - `scripts/build_corruption_grid.py`: `3a06169d3f25fdf2ef313b9b9b6ae25cb5c9f43ba6ce39e723d9b4b509dce7d2`
  - `tests/test_corruption_parameterization.py`: `8b7133e6c34cb5bbc1ef2c3a0ff94bf9d733b458367f73ea5c9b9abc360fa6ce`
  - `tests/test_corruption_determinism.py`: `2e3536c66f6dbf91264318107afd49878da8cc49e65c9c7e1c65b3caf515b4f5`
  - `tests/test_corruption_label_cleanliness.py`: `ea65a09f20f9ba4b3bd3268043c6848c72a57c11fbe1b652973769f7dcde475d`
  - `tests/test_corruption_bounds.py`: `29e4f4feb097e5b8f6452503b87aa8c6fbf94a162c5b857206bd4adac68995b5`
  - `tests/test_corruption_manifest_schema.py`: `fc539c380dec52586d1bc9572ad2c9bbcb7a4d13851a2286e3d4a6c7670598b0`

Phase 2 console.log line inventory:

- `scripts/build_corruption_grid.py`
  - Comment line `21`: `# Phase 2 console.log: records corruption grid script dispatch.`
  - Code line `22`: `console.log("phase2.script.build_corruption_grid_dispatch", repo_root=str(repo_root), config=str(args.config))`
  - Comment line `25`: `# Phase 2 console.log: records corruption grid script completion.`
  - Code line `26`: `console.log("phase2.script.build_corruption_grid_complete", definitions=len(definitions), manifest_path=manifest["manifest_path"])`
- `src/mavs_ch10b/corruptions/base.py`
  - Comment line `102`: `# Phase 2 console.log: records corruption application dispatch.`
  - Code line `103`: `console.log(`
  - Comment line `113`: `# Phase 2 console.log: records corruption application completion.`
  - Code line `114`: `console.log(`
  - Comment line `155`: `# Phase 2 console.log: records applied corruption manifest construction.`
  - Code line `156`: `console.log("phase2.corruption.manifest_built", corruption_id=output.definition.corruption_id, manifest_hash=manifest["corruption_manifest_hash"])`
  - Comment line `184`: `# Phase 2 console.log: records deterministic RNG creation for a corruption run.`
  - Code line `185`: `console.log("phase2.corruption.rng_created", corruption_id=definition.corruption_id, derived_seed=seed)`
- `src/mavs_ch10b/corruptions/grid.py`
  - Comment line `20`: `# Phase 2 console.log: records corruption grid configuration loading.`
  - Code line `21`: `console.log("phase2.corruption.grid_config_loaded", path=str(resolved), families=len(config["corruption_families"]), levels=len(config["levels"]))`
  - Comment line `51`: `# Phase 2 console.log: records corruption grid expansion.`
  - Code line `52`: `console.log("phase2.corruption.grid_built", definitions=len(definitions), datasets=len(config["datasets"]), families=len(config["corruption_families"]))`
  - Comment line `114`: `# Phase 2 console.log: records corruption grid manifest persistence.`
  - Code line `115`: `console.log(`
  - Comment line `151`: `# Phase 2 console.log: records corruption manifest index CSV persistence.`
  - Code line `152`: `console.log("phase2.corruption.index_csv_written", path=str(path), rows=len(records))`
- `src/mavs_ch10b/corruptions/manifest.py`
  - Comment line `41`: `# Phase 2 console.log: records applied manifest schema validation.`
  - Code line `42`: `console.log("phase2.corruption.applied_manifest_validated", corruption_id=manifest["corruption_id"], fields=len(manifest))`
  - Comment line `51`: `# Phase 2 console.log: records applied corruption manifest persistence.`
  - Code line `52`: `console.log("phase2.corruption.applied_manifest_written", path=str(path), corruption_id=manifest["corruption_id"])`
- `src/mavs_ch10b/corruptions/registry.py`
  - Comment line `57`: `# Phase 2 console.log: records corruption registry construction.`
  - Code line `58`: `console.log("phase2.corruption.registry_built", families=list(registry))`
  - Comment line `68`: `# Phase 2 console.log: records corruption configuration loading.`
  - Code line `69`: `console.log("phase2.corruption.config_loaded", path=str(path), family=config["corruption_family"])`

WorkPlan compliance:

- Followed Phase 2 scope: built a deterministic corruption framework without changing Chapter 10A training.
- Implemented every required corruption family from `WorkPlan.md`.
- Every family supports `level=0.0` and `level=1.0`.
- Built the fixed level grid and seed lists exactly as specified in `WorkPlan.md`.
- Generated corruption manifests for all dataset, split, family, level, and seed-role combinations.
- Added tests proving registration, parameterization, determinism, label cleanliness, numeric bounds, manifest schema, and Chapter 10A artifact immutability.
- Added `console.log(...)` calls with identifying comments at every Phase 2 orchestration step, registry step, grid step, corruption application step, RNG step, and manifest step.
- Documented files, configs, grid choices, seed lists, tests, generated manifest hashes, and deviations here as required.

Deviations:

- None from Phase 2 acceptance criteria.
- The implementation uses processed-feature corruption proxies because Phase 2 operates on frozen Chapter 10A processed benchmark bundles and must not refit preprocessing or checkpoints. This is allowed by `WorkPlan.md` for cases where only processed arrays are available.
- An initial label-cleanliness test assumed all non-label corruptions preserve the full row count. It was corrected because `distribution_shift` intentionally returns a selected row subset while preserving row-id traceability and labels for selected rows.
- An initial external stress-audit counting rule failed because it counted only single-line `console.log("phase2...")` calls and missed multiline `console.log(` calls. The audit was rerun with comment-based counting, which matches the stated requirement that each `console.log` has an identifying comment.

Risks or limitations:

- Phase 2 only creates corruption definitions and corruption transformation code. It does not yet run the imported Chapter 10A systems under the full corruption matrix; that belongs to Phase 3.
- Feature-space corruptions currently operate on processed numeric arrays. Raw categorical corruption is intentionally not implemented to avoid invalid categories.
- Distribution shift uses a deterministic feature-norm slice until richer dataset subgroup metadata is wired into later phases.
- Specialist failure currently implements the required constant-uncertainty failure mode. Additional failure modes can be added later only as exploratory unless the full suite is rerun from frozen configs.

Next required action:

- Begin Phase 3 from `WorkPlan.md`: Governance Stress Testing Matrix.

### Phase 3 - Governance Stress Testing Matrix

Date:

- 2026-06-21 15:25:06 +05:00

Files created or changed:

- Experiment configs:
  - `configs/experiments/locked_corruption_benchmark.yaml`
  - `configs/experiments/audit_corruption_benchmark.yaml`
- Stress runner source:
  - `src/mavs_ch10b/stress/__init__.py`
  - `src/mavs_ch10b/stress/cache.py`
  - `src/mavs_ch10b/stress/system_executor.py`
  - `src/mavs_ch10b/stress/trace_writer.py`
  - `src/mavs_ch10b/stress/run_manifest.py`
  - `src/mavs_ch10b/stress/run_matrix.py`
- Scripts:
  - `scripts/run_locked_corruption_benchmark.py`
  - `scripts/run_audit_corruption_benchmark.py`
- Result placeholders and git tracking rules:
  - `results/stress_runs/.gitkeep`
  - `results/corruption_traces/.gitkeep`
  - `.gitignore`
- Tests:
  - `tests/test_stress_matrix_complete.py`
  - `tests/test_systems_use_identical_corrupted_inputs.py`
  - `tests/test_all_specialists_still_speak_under_corruption.py`
  - `tests/test_corruption_trace_alignment.py`
  - `tests/test_audit_seed_independence.py`

Code produced:

- Added `StressCache`.
  - Loads each clean Chapter 10A benchmark bundle once per dataset and split.
  - Loads frozen Chapter 10A specialist checkpoints only for corrupted-feature inference.
  - Caches specialist predictions by dataset id and corrupted feature hash so deterministic repeated feature corruptions do not rerun equivalent specialist inference.
  - Loads processed feature names from Chapter 10A feature-name artifacts when available, falling back to stable processed-column ids.
- Added `system_executor`.
  - Builds `CorruptionInput` from frozen Chapter 10A benchmark features, labels, specialist probabilities, and supports.
  - Applies the Phase 2 corruption object.
  - For input-space corruptions, rebuilds specialist probabilities and supports from corrupted processed features using frozen checkpoints.
  - For score-space, label-space, and row-space corruptions, uses the corrupted score/label/row arrays without changing checkpoints or system configs.
  - Constructs a Chapter 10A-compatible `SpecialistOutputBundle`.
  - Runs every comparison system on the same prepared corrupted bundle.
  - Writes applied corruption manifests before any system execution for that corruption cell.
- Added `trace_writer`.
  - Writes deterministic `.npz` prediction artifacts per system run.
  - Writes deterministic columnar `.npz` governance trace artifacts for `veto_mavs` and `pure_mavs_gc`.
  - The columnar governance trace metadata records every inherited Chapter 10A trace field and every required Chapter 10B stress trace field.
  - Columnar traces were used instead of row-by-row JSONL because the full Phase 3 matrix produces tens of millions of governance rows. The field schema remains explicit and row-aligned.
- Added `run_manifest`.
  - Enforces the Phase 1 import manifest hash guard.
  - Distinguishes `exploratory` from `final` runs.
  - Refuses final mode if corruption configs or corruption manifests are uncommitted.
  - Writes prediction, trace, and aggregate indexes plus run manifests.
- Added `run_matrix`.
  - Selects locked or audit definitions from the Phase 2 corruption grid.
  - Runs all five required comparison systems:
    - `single_model`
    - `mean_ensemble`
    - `static_weighted_ensemble`
    - `veto_mavs`
    - `pure_mavs_gc`
  - Preserves identical corrupted input/score bundles across all systems for the same dataset, split, corruption family, level, and seed.
  - Produces seed-level rows and aggregate rows.

Commands run:

- Smoke run before full matrix:
  - `$env:PYTHONPATH='src'; python scripts\run_locked_corruption_benchmark.py --run-id phase3_locked_smoke --max-definitions 1`
  - Result: passed; produced 5 prediction artifacts and 2 governance trace artifacts for one locked corruption definition.
- Smoke run after switching governance traces to columnar `.npz`:
  - `$env:PYTHONPATH='src'; python scripts\run_locked_corruption_benchmark.py --run-id phase3_locked_smoke_npz --max-definitions 1`
  - Result: passed; produced 5 prediction artifacts and 2 columnar governance trace artifacts.
- Locked full benchmark:
  - `$env:PYTHONPATH='src'; python scripts\run_locked_corruption_benchmark.py`
  - Run id: `phase3_locked_full_v1`
  - Result: complete.
- Audit full benchmark:
  - `$env:PYTHONPATH='src'; python scripts\run_audit_corruption_benchmark.py`
  - Run id: `phase3_audit_full_v1`
  - Result: complete.
- Full automated tests:
  - `$env:PYTHONPATH='src'; python -m pytest -q -p no:cacheprovider`
  - Result: `23 passed in 3.70s`.
- Independent Phase 3 stress audit:
  - Verified locked and audit manifest completeness, prediction index hashes, trace index hashes, aggregate index hashes, sampled prediction and trace artifact hashes, trace/prediction row alignment, columnar trace schema metadata, identical corrupted bundle hashes across systems, locked/audit seed independence, Chapter 10A artifact immutability, and absence of Chapter 10B `.joblib` artifacts.
  - Result: `PHASE3_STRESS_AUDIT PASS`.
- ASCII audit:
  - Result: `ASCII_CHECK PASS`.
- Console comment audit:
  - Result: `CONSOLE_COMMENT_CHECK PASS`.

Datasets touched:

- No Chapter 10A dataset file was modified.
- Locked and audit benchmark splits were evaluated for:
  - `breast_cancer_wisconsin`
  - `adult_income`
  - `credit_card_fraud`
  - `bank_marketing`
- Benchmark evidence came only from Chapter 10A locked and audit benchmark splits.
- Train, validation, and calibration splits were not used for Phase 3 robustness evidence.

Models imported, trained, or evaluated:

- No model was trained.
- No specialist checkpoint was changed.
- No system config, static weight, governance threshold, or MAVS coefficient was changed.
- Frozen specialists were evaluated under input-space corruptions only for inference on corrupted processed features.
- Score-space, label-space, and row-space corruptions reused or transformed frozen specialist-output bundles without checkpoint mutation.
- No `.joblib` artifact exists under Chapter 10B `results/`.

Corruption families touched:

- All nine required corruption families were run across locked and audit matrices:
  - `feature_noise`
  - `missing_features`
  - `random_feature_deletion`
  - `label_noise`
  - `confidence_distortion`
  - `adversarial_confidence_inflation`
  - `distribution_shift`
  - `synthetic_sensor_failure`
  - `specialist_failure`
- Every deterministic family still records a seed and produces a run manifest entry.
- Every stochastic family has seed-level outputs.
- Aggregate index rows exist for each dataset, split, system, corruption family, level, and seed role.

Benchmark/test outputs:

- Locked full run:
  - Run id: `phase3_locked_full_v1`
  - Run mode: `exploratory`
  - System runs: `7200`
  - Governance trace artifacts: `2880`
  - Aggregate rows: `2880`
  - Prediction rows: `66355600`
  - Governance trace rows: `26542240`
  - Prediction artifact root: `results/stress_runs/phase3_locked_full_v1/predictions/`
  - Applied manifest root: `results/stress_runs/phase3_locked_full_v1/applied_manifests/`
  - Governance trace root: `results/corruption_traces/phase3_locked_full_v1/traces/`
  - Output size under `results/stress_runs/phase3_locked_full_v1`: `525860826` bytes across `8640` files.
  - Output size under `results/corruption_traces/phase3_locked_full_v1`: `3315411713` bytes across `2880` files.
- Audit full run:
  - Run id: `phase3_audit_full_v1`
  - Run mode: `exploratory`
  - System runs: `7200`
  - Governance trace artifacts: `2880`
  - Aggregate rows: `2880`
  - Prediction rows: `33177100`
  - Governance trace rows: `13270840`
  - Prediction artifact root: `results/stress_runs/phase3_audit_full_v1/predictions/`
  - Applied manifest root: `results/stress_runs/phase3_audit_full_v1/applied_manifests/`
  - Governance trace root: `results/corruption_traces/phase3_audit_full_v1/traces/`
  - Output size under `results/stress_runs/phase3_audit_full_v1`: `271485459` bytes across `8640` files.
  - Output size under `results/corruption_traces/phase3_audit_full_v1`: `1671013238` bytes across `2880` files.
- Full pytest:
  - `23 passed in 3.70s`
- Phase 3 stress audit:
  - `PHASE3_STRESS_AUDIT PASS`
  - `locked_prediction_rows 66355600`
  - `locked_trace_rows 26542240`
  - `audit_prediction_rows 33177100`
  - `audit_trace_rows 13270840`
  - `console_log_calls 78`
  - `phase3_console_log_comments 31`

Artifact hashes:

- Phase 3 config hashes:
  - `configs/experiments/locked_corruption_benchmark.yaml`: `055eb2d4b19e0d1a8eade836fdeb8696b6fabec4ef462dbd53f5668415cff50f`
  - `configs/experiments/audit_corruption_benchmark.yaml`: `a71ddb487f565961f8a6cef952cbe575b222ef438d72bd45fe4e3f532634b6db`
- Phase 3 source hashes:
  - `src/mavs_ch10b/stress/__init__.py`: `eed954edaf8e4f08f5a7e10a088d8dbe91880519317e3db93534318bab8a762f`
  - `src/mavs_ch10b/stress/cache.py`: `122bd226a7f458007b9209215d83ea9cbfe2a0237cc32fbb2ded510c6a77cf7b`
  - `src/mavs_ch10b/stress/system_executor.py`: `bc92069aae02f8794464d92614ad4f0feaf4e161b86db390bc9f22ce72a6ff5b`
  - `src/mavs_ch10b/stress/trace_writer.py`: `4d718d251c31647c800b22cffb4ac7583000d9ad40855e5a589cd69d8dd47c73`
  - `src/mavs_ch10b/stress/run_manifest.py`: `db9e81be9915d8a9e4369fb0256cc11132890f5a4a90c350320caebbb348867b`
  - `src/mavs_ch10b/stress/run_matrix.py`: `1fa06482356bf9449d91424d1647d491f584f7aeb77200424a70a770e22f11bd`
  - `scripts/run_locked_corruption_benchmark.py`: `c4fb902af9de54b345930518f22a37bd17e70ce983ca3c6b85c4961aaf92c5df`
  - `scripts/run_audit_corruption_benchmark.py`: `78eecd89172dbc8b9b22c751a096eb3f5841306d3a8b58fb0191bee94b5fb661`
- Phase 3 test hashes:
  - `tests/test_stress_matrix_complete.py`: `d12c73edafa3f3ae137e37e6b2ff6f3c669c2076e885e174a19e78c7988509de`
  - `tests/test_systems_use_identical_corrupted_inputs.py`: `6d95782dcd776270a44db908fbe0686fb367158e268e5e1ba3c7d6101c88bc42`
  - `tests/test_all_specialists_still_speak_under_corruption.py`: `af63123a7ba44d6b59dc47b57a737edde320645367f0b3cd8d1af36650d7cae1`
  - `tests/test_corruption_trace_alignment.py`: `f7c739001f9f54cdb8c6a272afbf060732e84937283a407f24a73fe6f40af6f7`
  - `tests/test_audit_seed_independence.py`: `219bf69a97ad06ec8666a167b1b3bce1de0ce33d8915e4802f2565c8801e6ebb`
- Locked run artifact hashes:
  - `results/stress_runs/phase3_locked_full_v1_run_manifest.json`: `c19f1cf6d380a79701ef7de4a6a84ea4ca834dbc81707594d6bec1d11bb65350`
  - `results/stress_runs/phase3_locked_full_v1_prediction_index.csv`: `ee8a12c7a669877b4ffdefbbfdf016eec525348d309e82de5fef5f57a634bce4`
  - `results/stress_runs/phase3_locked_full_v1_trace_index.csv`: `9565b0e6f9164ac2c9262b5f0d61d7495b53e2f3c2575c95c777a194b81acef0`
  - `results/stress_runs/phase3_locked_full_v1_aggregate_index.csv`: `c490afee985775ec1f5cca73ae67010c0513ef87e9508cf74141eeaa0c6ddab5`
- Audit run artifact hashes:
  - `results/stress_runs/phase3_audit_full_v1_run_manifest.json`: `5c52ae245933cc3d90c974faa37e86bdcbf889c06ad181ee8133a8267f8d42e7`
  - `results/stress_runs/phase3_audit_full_v1_prediction_index.csv`: `72d5163268fedac421946bb2aa8949a280f417ba687c62af49a25522d403174c`
  - `results/stress_runs/phase3_audit_full_v1_trace_index.csv`: `f9a4aac2bf81661f157648c7e4100311d2b3b3f325a67e6a5c7be80ad3aac2cd`
  - `results/stress_runs/phase3_audit_full_v1_aggregate_index.csv`: `9fcdc179a6af2a3e25db8e8cb1cbbab9e1eb1575f1c7de73f65263d22c3df056`

Phase 3 console.log line inventory:

- `scripts/run_locked_corruption_benchmark.py`
  - Comment line `19`: `# Phase 3 console.log: records locked corruption benchmark script dispatch.`
  - Code line `20`: `console.log("phase3.script.locked_dispatch", repo_root=str(repo_root), config=str(args.config), run_id=args.run_id)`
  - Comment line `28`: `# Phase 3 console.log: records locked corruption benchmark script completion.`
  - Code line `29`: `console.log("phase3.script.locked_complete", run_id=manifest["run_id"], system_runs=manifest["system_run_count"], manifest_path=manifest["manifest_path"])`
- `scripts/run_audit_corruption_benchmark.py`
  - Comment line `19`: `# Phase 3 console.log: records audit corruption benchmark script dispatch.`
  - Code line `20`: `console.log("phase3.script.audit_dispatch", repo_root=str(repo_root), config=str(args.config), run_id=args.run_id)`
  - Comment line `28`: `# Phase 3 console.log: records audit corruption benchmark script completion.`
  - Code line `29`: `console.log("phase3.script.audit_complete", run_id=manifest["run_id"], system_runs=manifest["system_run_count"], manifest_path=manifest["manifest_path"])`
- `src/mavs_ch10b/stress/cache.py`
  - Comment line `36`: `# Phase 3 console.log: records cache reuse for a clean benchmark bundle.`
  - Code line `37`: `console.log("phase3.cache.clean_bundle_reused", dataset_id=dataset_id, split=split)`
  - Comment line `39`: `# Phase 3 console.log: records cache loading for a clean benchmark bundle.`
  - Code line `40`: `console.log("phase3.cache.clean_bundle_load_start", dataset_id=dataset_id, split=split)`
  - Comment line `56`: `# Phase 3 console.log: records cache completion for a clean benchmark bundle.`
  - Code line `57`: `console.log(`
  - Comment line `75`: `# Phase 3 console.log: records specialist prediction cache reuse for a repeated corrupted feature matrix.`
  - Code line `76`: `console.log("phase3.cache.specialist_prediction_reused", dataset_id=dataset_id, rows=int(features.shape[0]), feature_hash=feature_hash)`
  - Comment line `81`: `# Phase 3 console.log: records specialist prediction dispatch for corrupted input features.`
  - Code line `82`: `console.log("phase3.cache.specialist_predict_start", dataset_id=dataset_id, rows=int(features.shape[0]), feature_hash=feature_hash)`
  - Comment line `97`: `# Phase 3 console.log: records specialist prediction completion for corrupted input features.`
  - Code line `98`: `console.log(`
  - Comment line `115`: `# Phase 3 console.log: records frozen specialist checkpoint loading for corrupted-feature inference.`
  - Code line `116`: `console.log("phase3.cache.specialist_loaded", dataset_id=dataset_id, specialist_id=specialist_id, checkpoint_path=str(checkpoint_path))`
- `src/mavs_ch10b/stress/system_executor.py`
  - Comment line `44`: `# Phase 3 console.log: records corruption preparation dispatch before system execution.`
  - Code line `45`: `console.log(`
  - Comment line `89`: `# Phase 3 console.log: records corruption preparation completion before shared system execution.`
  - Code line `90`: `console.log(`
  - Comment line `109`: `# Phase 3 console.log: records system execution dispatch on a shared corrupted bundle.`
  - Code line `110`: `console.log(`
  - Comment line `121`: `# Phase 3 console.log: records system execution completion on a shared corrupted bundle.`
  - Code line `122`: `console.log(`
- `src/mavs_ch10b/stress/run_manifest.py`
  - Comment line `18`: `# Phase 3 console.log: records final-mode import manifest guard evaluation.`
  - Code line `19`: `console.log(`
  - Comment line `39`: `# Phase 3 console.log: records final-mode corruption config git cleanliness guard evaluation.`
  - Code line `40`: `console.log("phase3.run_manifest.corruption_config_git_guard", dirty=dirty, passed=not dirty)`
  - Comment line `85`: `# Phase 3 console.log: records aggregate seed-level index construction.`
  - Code line `86`: `console.log("phase3.run_manifest.aggregate_rows_built", rows=len(rows))`
  - Comment line `146`: `# Phase 3 console.log: records Phase 3 run manifest persistence.`
  - Code line `147`: `console.log(`
  - Comment line `166`: `# Phase 3 console.log: records Phase 3 manifest CSV persistence.`
  - Code line `167`: `console.log("phase3.run_manifest.csv_written", path=str(path), rows=len(records))`
- `src/mavs_ch10b/stress/run_matrix.py`
  - Comment line `31`: `# Phase 3 console.log: records stress experiment configuration loading.`
  - Code line `32`: `console.log("phase3.run_matrix.config_loaded", path=str(resolved), run_id=config["run_id"], split_label=config["split_label"])`
  - Comment line `57`: `# Phase 3 console.log: records stress matrix dispatch.`
  - Code line `58`: `console.log(`
  - Comment line `93`: `# Phase 3 console.log: records one corruption cell dispatch across all comparison systems.`
  - Code line `94`: `console.log(`
  - Comment line `129`: `# Phase 3 console.log: records one corruption cell completion across all comparison systems.`
  - Code line `130`: `console.log("phase3.run_matrix.definition_complete", run_id=run_id_value, corruption_id=definition.corruption_id, systems=len(systems))`
  - Comment line `143`: `# Phase 3 console.log: records stress matrix completion.`
  - Code line `144`: `console.log(`
- `src/mavs_ch10b/stress/trace_writer.py`
  - Comment line `47`: `# Phase 3 console.log: records prediction artifact persistence dispatch.`
  - Code line `48`: `console.log("phase3.trace_writer.prediction_write_start", path=str(path), system_id=output.system_id, rows=int(arrays["row_ids"].shape[0]))`
  - Comment line `56`: `# Phase 3 console.log: records prediction artifact persistence completion.`
  - Code line `57`: `console.log("phase3.trace_writer.prediction_write_complete", path=str(path), sha256=record["prediction_sha256"], rows=record["prediction_rows"])`
  - Comment line `64`: `# Phase 3 console.log: records governance trace artifact persistence dispatch.`
  - Code line `65`: `console.log("phase3.trace_writer.trace_write_start", path=str(path), system_id=output.system_id, traces=len(output.traces))`
  - Comment line `81`: `# Phase 3 console.log: records governance trace artifact persistence completion.`
  - Code line `82`: `console.log("phase3.trace_writer.trace_write_complete", path=str(path), sha256=record["trace_sha256"], rows=row_count)`
  - Comment line `140`: `# Phase 3 console.log: records conversion of row governance traces into columnar stress traces.`
  - Code line `141`: `console.log("phase3.trace_writer.trace_columnar_payload_built", system_id=output.system_id, rows=rows, fields=len(metadata["fields"]))`
  - Comment line `187`: `# Phase 3 console.log: records Phase 3 CSV index persistence.`
  - Code line `188`: `console.log("phase3.trace_writer.csv_written", path=str(path), rows=len(records))`

WorkPlan compliance:

- Followed Phase 3 scope by running all imported comparison systems through all required corruption regimes for locked and audit benchmark splits.
- Included every comparison system required by the Chapter 10B document and the research bible.
- Used frozen Chapter 10A specialists, static weights, single-model selections, governance configs, and checkpoints.
- Did not train, tune, or modify any model or governance coefficient.
- Rebuilt specialist outputs from corrupted processed features for input-space corruptions.
- Reused identical corrupted input/score bundles across all systems for each corruption cell; tests and stress audit verified this by `corrupted_input_bundle_hash`.
- Wrote prediction outputs for all systems.
- Wrote governance trace artifacts for `veto_mavs` and `pure_mavs_gc`.
- Wrote run manifests with run id, run mode, git commit, Chapter 10A import manifest hash, corruption grid hash, system ids, output artifact hashes, command line, dependency versions, and row counts.
- Added tests proving matrix completeness, identical corrupted inputs, all-specialists-still-speak behavior, trace alignment, and locked/audit seed independence.

Deviations:

- Full runs were executed in `exploratory` mode, not `final` mode, because the current repository contains uncommitted Phase 1-3 implementation files. This follows the anti-overfitting control: final mode is implemented and will refuse uncommitted corruption configs/manifests.
- Governance traces are stored as deterministic columnar `.npz` artifacts instead of row-by-row JSONL. This was necessary to make the full matrix practical at tens of millions of governance rows. Each artifact still records the full required trace schema in metadata and row-aligned arrays for inherited and stress fields.
- Prediction row totals are lower than the maximum no-shift count because `distribution_shift` intentionally reduces row counts while preserving row-id traceability.

Failed runs or reruns:

- No full locked or audit run failed.
- Two smoke runs were executed before the full matrix:
  - `phase3_locked_smoke`
  - `phase3_locked_smoke_npz`
- The second smoke run validated the final columnar trace format before full locked/audit execution.

Risks or limitations:

- Runtime emitted scikit-learn `InconsistentVersionWarning` messages because Chapter 10A checkpoints were produced with `sklearn 1.9.0` and this environment uses `sklearn 1.7.1`. Phase 1 clean replay reproduced Chapter 10A metrics exactly, and Phase 3 did not train or modify checkpoints.
- Phase 3 produces system outputs and governance traces, not robustness metrics or curves. Metric computation and robustness analysis remain Phase 4.
- Final-mode execution requires committing/fixing the current dirty research worktree first, as designed by the anti-overfitting guard.

Next required action:

- Begin Phase 4 from `WorkPlan.md`: Robustness Evaluation and Curves.

### Phase 4 - Robustness Evaluation and Curves

Date:

- 2026-06-21 15:58:01 +05:00

Files created or changed:

- `src/mavs_ch10b/evaluation/__init__.py`
- `src/mavs_ch10b/evaluation/metrics.py`
- `src/mavs_ch10b/evaluation/robustness_area.py`
- `src/mavs_ch10b/evaluation/safety.py`
- `src/mavs_ch10b/evaluation/aggregation.py`
- `src/mavs_ch10b/evaluation/statistics.py`
- `src/mavs_ch10b/evaluation/curve_builder.py`
- `scripts/build_robustness_metrics.py`
- `scripts/build_robustness_curves.py`
- `results/metrics/locked_corruption/.gitkeep`
- `results/metrics/audit_corruption/.gitkeep`
- `results/robustness_curves/.gitkeep`
- `results/figures/robustness_curves/.gitkeep`
- `tests/test_robustness_metric_definitions.py`
- `tests/test_unsafe_acceptance_metric.py`
- `tests/test_robustness_curve_area.py`
- `tests/test_threshold_distribution_metrics.py`
- `tests/test_metric_trace_alignment.py`
- `.gitignore`
- `Path.md`

Code produced:

- Added `mavs_ch10b.evaluation.metrics` to load every Phase 3 prediction `.npz`, compute clean-label accuracy, error rate, precision, recall, F1, observed-label accuracy/F1, unsafe acceptance, false positive rate, false negative rate, technical failure rate, rejection rate, conditional high-corruption unsafe acceptance, and deterministic row/decision/probability/label hashes.
- Added `mavs_ch10b.evaluation.safety` to isolate unsafe acceptance and conditional unsafe acceptance definitions.
- Added `mavs_ch10b.evaluation.aggregation` to build system summaries and governance-vs-baseline delta tables against `single_model`, `mean_ensemble`, and `static_weighted_ensemble`.
- Added `mavs_ch10b.evaluation.statistics` to build seed-level variance and paired bootstrap confidence intervals using corruption-seed-paired governance/baseline deltas.
- Added `mavs_ch10b.evaluation.robustness_area` to compute fixed trapezoidal robustness areas and record metric directionality.
- Added `mavs_ch10b.evaluation.curve_builder` to emit per dataset/system/corruption-family robustness curve CSVs and PNG figures.
- Added `scripts/build_robustness_metrics.py` to transform Phase 3 prediction and trace indexes into locked/audit metric rows, system summaries, governance severity distributions, threshold distributions, and metric manifests.
- Added `scripts/build_robustness_curves.py` to transform metric rows into curve CSVs, curve figures, area tables, governance deltas, seed variance, paired bootstrap CIs, and a curve manifest.
- Added Phase 4 tests for metric definitions, unsafe acceptance, robustness area directionality/integration, threshold distributions, and metric-trace alignment.
- Added `console.log` calls at every material Phase 4 build step, each preceded by a comment identifying why the log exists.

Commands run:

- `python -m compileall -q src\mavs_ch10b\evaluation scripts\build_robustness_metrics.py scripts\build_robustness_curves.py`
- `python scripts\build_robustness_metrics.py *> results\metrics\phase4_metrics_console.log`
- `python scripts\build_robustness_curves.py *> results\metrics\phase4_curves_console.log`
- `python -m pytest -q -p no:cacheprovider`
- Independent validation script over final artifacts checking row counts, prediction index alignment, trace index alignment, histogram row totals, manifest hashes, curve/figure counts, area directionality, and no `.joblib` files under `results/`.
- `rg -n "Phase 4 console\.log|console\.log\(" src\mavs_ch10b\evaluation scripts\build_robustness_metrics.py scripts\build_robustness_curves.py`
- `Get-FileHash -Algorithm SHA256` for Phase 4 source, test, and final artifact files.

Datasets touched:

- `adult_income`
- `bank_marketing`
- `breast_cancer_wisconsin`
- `credit_card_fraud`

Models imported, trained, or evaluated:

- No model was trained, tuned, or selected in Phase 4.
- Phase 4 evaluated frozen Phase 3 prediction artifacts for:
  - `single_model`
  - `mean_ensemble`
  - `static_weighted_ensemble`
  - `veto_mavs`
  - `pure_mavs_gc`
- Metric computation used the locked and audit prediction/trace indexes from Phase 3 and did not load or mutate Chapter 10A checkpoints.

Corruption families touched:

- `adversarial_confidence_inflation`
- `confidence_distortion`
- `distribution_shift`
- `feature_noise`
- `label_noise`
- `missing_features`
- `random_feature_deletion`
- `specialist_failure`
- `synthetic_sensor_failure`

Benchmark/test outputs:

- Compile check: `COMPILE_PASS`
- Full test suite: `32 passed in 4.64s`
- Independent final validation: `PASS`
- Locked metric rows: `7200`
- Audit metric rows: `7200`
- Locked governance severity distribution rows: `2880`
- Audit governance severity distribution rows: `2880`
- Locked governance threshold distribution rows: `2880`
- Audit governance threshold distribution rows: `2880`
- Locked system summary rows: `180`
- Audit system summary rows: `180`
- Locked governance delta rows: `43200`
- Audit governance delta rows: `43200`
- Locked paired bootstrap CI rows: `10368`
- Audit paired bootstrap CI rows: `10368`
- Locked seed variance rows: `2880`
- Audit seed variance rows: `2880`
- Robustness curve rows: `5760`
- Robustness area rows: `3600`
- Curve CSV files: `180`
- Curve PNG files: `180`
- Directionality values present: `context_dependent`, `higher_is_better`, `lower_is_better`
- `.joblib` files under `results/`: `0`
- Final metric console log bytes: `26507858`
- Final curve console log bytes: `238468`

Stress validation evidence:

- Metric rows were validated key-for-key against Phase 3 prediction indexes using `run_id`, `split_label`, `dataset_id`, `system_id`, `corruption_family`, `corruption_level`, `corruption_seed`, `seed_role`, `prediction_path`, and `prediction_sha256`.
- `evaluated_rows` was validated against Phase 3 `prediction_rows` for every metric row.
- Governance severity and threshold rows were validated key-for-key against Phase 3 trace indexes.
- Severity and threshold histogram count sums were validated against `trace_rows` for every trace distribution row.
- Metric manifests were validated against actual output file hashes and Phase 3 source index hashes.
- Curve manifest was validated against `metric_rows_loaded = 14400`, `curve_rows = 5760`, `area_rows = 3600`, and the actual area file hash.
- Every curve CSV was validated to contain `32` rows: two benchmark splits, two seed roles per split family grouping, and eight corruption levels.

Artifact hashes:

- `src/mavs_ch10b/evaluation/__init__.py`: `186f43fb0f8419529b0dd65f50d35c6cf88145d2595c318c950d87ed1f3408c6`
- `src/mavs_ch10b/evaluation/metrics.py`: `fe72effdc710279767c7172871519377048ccd92257b4f6a8e26b878b56c9e4e`
- `src/mavs_ch10b/evaluation/robustness_area.py`: `979cc774b10b3706dd2b35611164c882cb0beb8156d2c0ea28d8143a92b7798c`
- `src/mavs_ch10b/evaluation/safety.py`: `59fb0fdfd14f7953f885be14bedc0aa76a5feae8334680282c394ac02dcf7d59`
- `src/mavs_ch10b/evaluation/aggregation.py`: `826a782f8997e7e9405d8d7f1281e3b21068f4a391425df6aca1da60e13d6633`
- `src/mavs_ch10b/evaluation/statistics.py`: `5910eb6d37bf2d6c29cf49fb8428b93545bd235c70a7e5be4a0d6491fb30687f`
- `src/mavs_ch10b/evaluation/curve_builder.py`: `430bd98084988447d883fbab29ecd71ca721e9f41cbf464298adf5f89bab3d69`
- `scripts/build_robustness_metrics.py`: `95a6c0f23855b30469ffc8ae11984617817438cbf944ba0aa134b3b006d377b5`
- `scripts/build_robustness_curves.py`: `d469329e38762b290efd3dc396b48137c661e19aa0c26c301232d4f836845638`
- `tests/test_robustness_metric_definitions.py`: `30ffbb2fdb4c5c2d9bf6117003cda7f9c5ade83e40c99e454b0e3cf09bf7c36e`
- `tests/test_unsafe_acceptance_metric.py`: `698379582a4c53265859a2cc7c9c70240c00add005e4382afb9d2483e86b58b9`
- `tests/test_robustness_curve_area.py`: `2a8e9bc2a3d558b5de2c1e3d01aeb129a31ed2c48727333bc76fc2c98638a870`
- `tests/test_threshold_distribution_metrics.py`: `4c862cfd12777ceb5f24b07b54fc6f66b7c5fa460e2a25c1fdbb844af9e17f95`
- `tests/test_metric_trace_alignment.py`: `1078094bb6df96a4d58062ce3f6d6fc478ae7a56480d29bdc1b1edbeb777c387`
- `results/metrics/locked_corruption/metric_rows.csv`: `c6e1b8a598ddf4d84f7f8b23287b91d9568d41ae025d9226ed18ff36e86b0e26`
- `results/metrics/locked_corruption/system_summary.csv`: `7eb4a93365575ea3a50d97d5ff7cb97adc5d72d1e47805aa7b102b28c5953fcf`
- `results/metrics/locked_corruption/governance_severity_distribution.csv`: `6f61b6f085f40568a7ad8b032a735b65358476ea63452ffcc09b731a200b51f3`
- `results/metrics/locked_corruption/governance_threshold_distribution.csv`: `dd19e4c167f40a96f52d4172bc02d044e19daf5482baa332d6a352bf736d6f8d`
- `results/metrics/locked_corruption/governance_delta_table.csv`: `4b22a2c71453f5c7c9a0ae2e3ccdbe9a6d7e19467ab8480e6ee776eb6fb516a7`
- `results/metrics/locked_corruption/paired_bootstrap_cis.csv`: `967d33a585789d5740990f3e04d43f83b69c631382c6746e2bbb028d09a46760`
- `results/metrics/locked_corruption/seed_level_variance.csv`: `b6bf471568b2e3ebd1a816238903eb14a4b320d27d83d4db272ee411b6769779`
- `results/metrics/locked_corruption/metric_manifest.json`: `122ac2f11f7c2b0527b065ef54baa385153a1116e5e116fb68312e523629006c`
- `results/metrics/audit_corruption/metric_rows.csv`: `a8466327b36897270708bb8cf032cb5c3c3e69ea626dae0c81efb852031b1342`
- `results/metrics/audit_corruption/system_summary.csv`: `41bacdc9e7920d5ed94fc8fbf297f765cf2eaf761b6ff28c8f63ebc133e40e28`
- `results/metrics/audit_corruption/governance_severity_distribution.csv`: `4de44ba47d7a2a400cac92e09c51e6bec82912da7665485da1384d128aae8092`
- `results/metrics/audit_corruption/governance_threshold_distribution.csv`: `b47e2f87c8b70c437912831982bf51206f1c518c60a771ef4e787fdd3b013dee`
- `results/metrics/audit_corruption/governance_delta_table.csv`: `518214a57ad1c7068a5763fcc1f84fb1acca56e6dc0ecea35a4c59ba4f3a3616`
- `results/metrics/audit_corruption/paired_bootstrap_cis.csv`: `be082284e45f89e59d9219a5035cdb9f58f36ee22a0dd936661b82527ac78f99`
- `results/metrics/audit_corruption/seed_level_variance.csv`: `9c731858233488301bb5d741f0954c413bc1222dcfb918a1a4b10ebc972f8df6`
- `results/metrics/audit_corruption/metric_manifest.json`: `5acadca7565472ab7ad5bb503eb36723ed59534a221036d8347021a04be7cfb0`
- `results/robustness_curves/robustness_curve_area.csv`: `00c9b059275423f8414dc5cba9a945e4bb4cb0b849bfa2caf92a1ed77ba1b521`
- `results/robustness_curves/curve_manifest.json`: `99db1a51b35a3c7fda921249ac874df2b30accdddb0b08cb9a8b3e82d922840e`

Phase 4 console.log line and comment inventory:

- `scripts/build_robustness_metrics.py`
  - Comment line `27`: `# Phase 4 console.log: records robustness metric script dispatch.`
  - Code line `28`: `console.log("phase4.script.metrics_dispatch", repo_root=str(repo_root), split_labels=list(split_labels))`
  - Comment line `30`: `# Phase 4 console.log: records robustness metric script completion.`
  - Code line `31`: `console.log("phase4.script.metrics_complete", manifests=[manifest["manifest_path"] for manifest in manifests])`
  - Comment line `41`: `# Phase 4 console.log: records split-level metric build dispatch.`
  - Code line `42`: `console.log("phase4.metrics.split_start", split_label=split_label, prediction_index=str(prediction_index), trace_index=str(trace_index))`
  - Comment line `78`: `# Phase 4 console.log: records metric build progress for large Phase 3 indexes.`
  - Code line `79`: `console.log("phase4.metrics.progress", split_label=split_label, processed=index, total=len(prediction_rows))`
  - Comment line `114`: `# Phase 4 console.log: records split-level metric build completion.`
  - Code line `115`: `console.log("phase4.metrics.split_complete", split_label=split_label, metric_rows=len(metric_rows), severity_rows=len(severity_rows), manifest_path=str(manifest_path))`
  - Comment line `122`: `# Phase 4 console.log: records governance trace index loading for metric alignment.`
  - Code line `123`: `console.log("phase4.metrics.trace_index_loaded", path=str(path), rows=len(rows))`
  - Comment line `141`: `# Phase 4 console.log: records governance severity and threshold distribution computation.`
  - Code line `142`: `console.log("phase4.metrics.trace_distribution_computed", trace_path=str(trace_path), rows=int(severity.shape[0]), severity_high_unsafe=severity_high_unsafe)`
- `scripts/build_robustness_curves.py`
  - Comment line `24`: `# Phase 4 console.log: records robustness curve script dispatch.`
  - Code line `25`: `console.log("phase4.script.curves_dispatch", repo_root=str(repo_root), bootstrap_iterations=args.bootstrap_iterations)`
  - Comment line `53`: `# Phase 4 console.log: records robustness curve script completion.`
  - Code line `54`: `console.log("phase4.script.curves_complete", manifest_path=str(manifest_path), curve_rows=len(curve_rows), area_rows=curve_info["area_rows"])`
  - Comment line `64`: `# Phase 4 console.log: records metric row loading for robustness curve construction.`
  - Code line `65`: `console.log("phase4.script.metric_rows_loaded", rows=len(rows))`
- `src/mavs_ch10b/evaluation/metrics.py`
  - Comment line `57`: `# Phase 4 console.log: records prediction artifact loading for metric computation.`
  - Code line `58`: `console.log("phase4.metrics.prediction_load_start", path=str(path), corruption_level=corruption_level)`
  - Comment line `86`: `# Phase 4 console.log: records prediction metric computation completion.`
  - Code line `87`: `console.log("phase4.metrics.prediction_metrics_computed", path=str(path), rows=metrics.evaluated_rows, accuracy=metrics.accuracy, f1=metrics.f1)`
  - Comment line `195`: `# Phase 4 console.log: records metric CSV artifact persistence.`
  - Code line `196`: `console.log("phase4.metrics.csv_written", path=str(path), rows=len(records), sha256=hash_file(path))`
- `src/mavs_ch10b/evaluation/curve_builder.py`
  - Comment line `41`: `# Phase 4 console.log: records robustness curve row construction.`
  - Code line `42`: `console.log("phase4.curve_builder.curve_rows_built", rows=len(records))`
  - Comment line `64`: `# Phase 4 console.log: records robustness curve artifact persistence completion.`
  - Code line `65`: `console.log("phase4.curve_builder.artifacts_written", curve_files=len(curve_files), figure_files=len(figure_files), area_path=str(area_path))`
  - Comment line `100`: `# Phase 4 console.log: records robustness curve PNG persistence.`
  - Code line `101`: `console.log("phase4.curve_builder.figure_written", path=str(path), sha256=hash_file(path))`
- `src/mavs_ch10b/evaluation/statistics.py`
  - Comment line `33`: `# Phase 4 console.log: records seed-level variance table construction.`
  - Code line `34`: `console.log("phase4.statistics.seed_variance_built", rows=len(records))`
  - Comment line `97`: `# Phase 4 console.log: records paired bootstrap CI table construction.`
  - Code line `98`: `console.log("phase4.statistics.bootstrap_cis_built", rows=len(records), iterations=iterations)`
- `src/mavs_ch10b/evaluation/aggregation.py`
  - Comment line `36`: `# Phase 4 console.log: records construction of system-level metric summaries.`
  - Code line `37`: `console.log("phase4.aggregation.system_summary_built", rows=len(records))`
  - Comment line `79`: `# Phase 4 console.log: records construction of governance-vs-baseline delta table.`
  - Code line `80`: `console.log("phase4.aggregation.governance_delta_built", rows=len(records))`
- `src/mavs_ch10b/evaluation/robustness_area.py`
  - Comment line `55`: `# Phase 4 console.log: records robustness curve area computation.`
  - Code line `56`: `console.log("phase4.robustness_area.rows_built", rows=len(records))`

WorkPlan compliance:

- Followed Phase 4 scope by computing robustness metrics and generating `results/robustness_curves/`.
- Produced metric computation for every dataset, split, system, corruption family, corruption level, and seed present in the full Phase 3 locked/audit stress indexes.
- Used clean labels for primary accuracy and F1, and labeled observed-label metrics separately.
- Used unsafe acceptance definition `count(decision == 1 and y_clean == 0) / count(y_clean == 0)`.
- Reported conditional unsafe acceptance under high corruption levels and under high governance severity where applicable.
- Kept technical failure rate separate from error rate.
- Used Chapter 10A binary decision convention for rejection rate.
- Computed trapezoidal robustness area over the configured corruption levels and recorded directionality for every area row.
- Generated governance severity and threshold distributions from governance trace artifacts.
- Added paired bootstrap confidence intervals, seed-level variance, and governance-vs-baseline delta tables.
- Did not train models or tune thresholds on locked or audit results.
- `Path.md` now records commands, artifact paths, row counts, hashes, tests, deviations, and console.log line/comment inventory.

Deviations:

- Paired bootstrap confidence intervals are seed-level paired by `corruption_seed`, not row-level bootstrap over individual examples. This follows the WorkPlan condition "where row alignment permits": row alignment is validated separately against Phase 3 prediction/trace indexes, while seed-level pairing avoids loading tens of millions of example-level rows for every governance/baseline/metric comparison and preserves independent locked/audit seed structure.
- Robustness figures are generated as PNG files through matplotlib in addition to the required curve CSVs.
- `high_corruption_unsafe_acceptance_rate` is numeric for every row. Non-high corruption levels record `0.0`; system summaries average that metric only for rows with `corruption_level >= 0.8`, preserving the high-corruption interpretation without leaving missing metric fields.

Failed runs or reruns:

- The first curve build produced the main curve files but failed while writing paired bootstrap CIs because `corruption_seed` was indexed as a string and looked up as an integer. Fixed `src/mavs_ch10b/evaluation/statistics.py` to keep seed keys as strings and reran the curve build successfully.
- The first independent validation found blank `high_corruption_unsafe_acceptance_rate` values on low-corruption rows. Fixed `src/mavs_ch10b/evaluation/metrics.py` to emit numeric values for every row and fixed `src/mavs_ch10b/evaluation/aggregation.py` to keep the high-corruption summary high-level-only. Regenerated metric and curve artifacts, then reran tests and validation successfully.

Risks or limitations:

- Phase 4 computes robustness evidence from Phase 3 artifacts only. Any claim about narrative robustness conclusions remains deferred to Phase 5 reporting.
- The full metric console log is intentionally large because every prediction load and metric computation is logged as requested.
- The repository remains an uncommitted research worktree; final-mode claims should be made only after committing/fixing the research state.

Next required action:

- Begin Phase 5 from `WorkPlan.md`: analysis, corruption atlas, failure map, and robustness report.

## Update Template for Future Work

Use this template for every material implementation update:

```text
### <Phase Name> - <Short Change Title>

Date:

Files created or changed:

Code produced:

Commands run:

Datasets touched:

Models imported, trained, or evaluated:

Corruption families touched:

Benchmark/test outputs:

Artifact hashes:

WorkPlan compliance:

Deviations:

Risks or limitations:

Next required action:
```

## Non-Negotiable Tracking Rules

- Do not mark a phase complete unless its acceptance criteria in `WorkPlan.md` are satisfied.
- Do not retrain models for Chapter 10B unless explicitly reconstructing missing Chapter 10A artifacts under the no-retraining policy.
- Do not tune models, ensemble weights, governance thresholds, corruption levels, corruption seeds, or MAVS coefficients on locked or audit corruption results.
- Do not mix training diagnostics with final robustness evidence.
- Do not claim MAVS-GC improves robustness unless the claim is supported against multiple baselines and documented with benchmark artifacts.
- Do not omit negative or neutral results.
- Every corruption run must record dataset hashes, split hashes, checkpoint hashes, config hashes, corruption manifest hashes, command line, and git commit.
- Every future implementation update must state whether it followed `WorkPlan.md` or deviated from it.
