from __future__ import annotations

import pytest

from mavs_ch10b.verification.import_audit import validate_no_training_command


def test_no_retraining_guard_allows_phase1_scripts() -> None:
    validate_no_training_command(["import_ch10a_foundation.py"])
    validate_no_training_command(["run_clean_baseline.py"])


def test_no_retraining_guard_blocks_training_scripts() -> None:
    with pytest.raises(ValueError):
        validate_no_training_command(["python", "scripts/train_specialists.py"])
    with pytest.raises(ValueError):
        validate_no_training_command(["python", "scripts/prepare_datasets.py"])

