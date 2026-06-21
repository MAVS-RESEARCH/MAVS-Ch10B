from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from mavs_ch10b.verification.hash_utils import console, hash_file, hash_json


METRIC_COLUMNS: tuple[str, ...] = (
    "accuracy",
    "error_rate",
    "precision",
    "recall",
    "f1",
    "observed_label_accuracy",
    "observed_label_f1",
    "unsafe_acceptance_rate",
    "false_positive_rate",
    "false_negative_rate",
    "technical_failure_rate",
    "rejection_rate",
    "high_corruption_unsafe_acceptance_rate",
)


@dataclass(frozen=True)
class PredictionMetrics:
    evaluated_rows: int
    positive_clean: int
    negative_clean: int
    decision_positive: int
    decision_negative: int
    true_positive: int
    false_positive: int
    true_negative: int
    false_negative: int
    accuracy: float
    error_rate: float
    precision: float
    recall: float
    f1: float
    observed_label_accuracy: float
    observed_label_f1: float
    unsafe_acceptance_rate: float
    false_positive_rate: float
    false_negative_rate: float
    technical_failure_rate: float
    rejection_rate: float
    high_corruption_unsafe_acceptance_rate: float


def compute_prediction_metrics(path: Path, corruption_level: float) -> tuple[PredictionMetrics, dict[str, str]]:
    # Phase 4 console.log: records prediction artifact loading for metric computation.
    console.log("phase4.metrics.prediction_load_start", path=str(path), corruption_level=corruption_level)
    try:
        with np.load(path) as loaded:
            probabilities = np.asarray(loaded["probabilities"], dtype=np.float64)
            decisions = np.asarray(loaded["decisions"], dtype=np.int8)
            y_clean = np.asarray(loaded["y_clean"], dtype=np.int8)
            y_observed = np.asarray(loaded["y_observed"], dtype=np.int8)
            row_ids = np.asarray(loaded["row_ids"])
    except Exception:
        metrics = _technical_failure_metrics()
        return metrics, {"row_hash": "", "decision_hash": "", "probability_hash": "", "label_hash": ""}
    valid = (
        decisions.shape == y_clean.shape
        and probabilities.shape == y_clean.shape
        and row_ids.shape == y_clean.shape
        and np.all(np.isfinite(probabilities))
        and np.all((probabilities >= 0.0) & (probabilities <= 1.0))
    )
    if not valid:
        metrics = _technical_failure_metrics()
        return metrics, {"row_hash": "", "decision_hash": "", "probability_hash": "", "label_hash": ""}
    metrics = metrics_from_arrays(decisions=decisions, y_clean=y_clean, y_observed=y_observed, corruption_level=corruption_level)
    hashes = {
        "row_hash": array_hash(row_ids),
        "decision_hash": array_hash(decisions),
        "probability_hash": array_hash(probabilities),
        "label_hash": array_hash(y_clean),
    }
    # Phase 4 console.log: records prediction metric computation completion.
    console.log("phase4.metrics.prediction_metrics_computed", path=str(path), rows=metrics.evaluated_rows, accuracy=metrics.accuracy, f1=metrics.f1)
    return metrics, hashes


def metrics_from_arrays(*, decisions: np.ndarray, y_clean: np.ndarray, y_observed: np.ndarray, corruption_level: float) -> PredictionMetrics:
    decisions = decisions.astype(np.int8)
    y_clean = y_clean.astype(np.int8)
    y_observed = y_observed.astype(np.int8)
    rows = int(y_clean.shape[0])
    tp = int(np.sum((decisions == 1) & (y_clean == 1)))
    fp = int(np.sum((decisions == 1) & (y_clean == 0)))
    tn = int(np.sum((decisions == 0) & (y_clean == 0)))
    fn = int(np.sum((decisions == 0) & (y_clean == 1)))
    positives = int(np.sum(y_clean == 1))
    negatives = int(np.sum(y_clean == 0))
    decision_positive = int(np.sum(decisions == 1))
    decision_negative = int(np.sum(decisions == 0))
    accuracy = safe_divide(tp + tn, rows)
    precision = safe_divide(tp, tp + fp)
    recall = safe_divide(tp, tp + fn)
    f1 = safe_divide(2.0 * precision * recall, precision + recall)
    observed_accuracy = safe_divide(int(np.sum(decisions == y_observed)), rows)
    observed_f1 = binary_f1(decisions, y_observed)
    unsafe_acceptance = safe_divide(fp, negatives)
    false_negative_rate = safe_divide(fn, positives)
    rejection_rate = safe_divide(decision_negative, rows)
    high_corruption_unsafe = unsafe_acceptance if float(corruption_level) >= 0.8 else 0.0
    return PredictionMetrics(
        evaluated_rows=rows,
        positive_clean=positives,
        negative_clean=negatives,
        decision_positive=decision_positive,
        decision_negative=decision_negative,
        true_positive=tp,
        false_positive=fp,
        true_negative=tn,
        false_negative=fn,
        accuracy=accuracy,
        error_rate=1.0 - accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
        observed_label_accuracy=observed_accuracy,
        observed_label_f1=observed_f1,
        unsafe_acceptance_rate=unsafe_acceptance,
        false_positive_rate=unsafe_acceptance,
        false_negative_rate=false_negative_rate,
        technical_failure_rate=0.0,
        rejection_rate=rejection_rate,
        high_corruption_unsafe_acceptance_rate=high_corruption_unsafe,
    )


def binary_f1(decisions: np.ndarray, labels: np.ndarray) -> float:
    tp = int(np.sum((decisions == 1) & (labels == 1)))
    fp = int(np.sum((decisions == 1) & (labels == 0)))
    fn = int(np.sum((decisions == 0) & (labels == 1)))
    precision = safe_divide(tp, tp + fp)
    recall = safe_divide(tp, tp + fn)
    return safe_divide(2.0 * precision * recall, precision + recall)


def safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return float(numerator) / float(denominator)


def metric_record(base: dict[str, Any], metrics: PredictionMetrics, hashes: dict[str, str]) -> dict[str, Any]:
    payload = {
        **base,
        "evaluated_rows": metrics.evaluated_rows,
        "positive_clean": metrics.positive_clean,
        "negative_clean": metrics.negative_clean,
        "decision_positive": metrics.decision_positive,
        "decision_negative": metrics.decision_negative,
        "true_positive": metrics.true_positive,
        "false_positive": metrics.false_positive,
        "true_negative": metrics.true_negative,
        "false_negative": metrics.false_negative,
        "accuracy": metrics.accuracy,
        "error_rate": metrics.error_rate,
        "precision": metrics.precision,
        "recall": metrics.recall,
        "f1": metrics.f1,
        "observed_label_accuracy": metrics.observed_label_accuracy,
        "observed_label_f1": metrics.observed_label_f1,
        "unsafe_acceptance_rate": metrics.unsafe_acceptance_rate,
        "false_positive_rate": metrics.false_positive_rate,
        "false_negative_rate": metrics.false_negative_rate,
        "technical_failure_rate": metrics.technical_failure_rate,
        "rejection_rate": metrics.rejection_rate,
        "high_corruption_unsafe_acceptance_rate": metrics.high_corruption_unsafe_acceptance_rate,
        **hashes,
    }
    payload["metric_row_hash"] = hash_json(payload)
    return payload


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    if not records:
        raise ValueError(f"No records to write: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(records[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    # Phase 4 console.log: records metric CSV artifact persistence.
    console.log("phase4.metrics.csv_written", path=str(path), rows=len(records), sha256=hash_file(path))


def array_hash(array: np.ndarray) -> str:
    import hashlib

    contiguous = np.ascontiguousarray(array)
    digest = hashlib.sha256()
    digest.update(str(contiguous.shape).encode("utf-8"))
    digest.update(str(contiguous.dtype).encode("utf-8"))
    digest.update(contiguous.tobytes())
    return digest.hexdigest()


def _technical_failure_metrics() -> PredictionMetrics:
    return PredictionMetrics(
        evaluated_rows=0,
        positive_clean=0,
        negative_clean=0,
        decision_positive=0,
        decision_negative=0,
        true_positive=0,
        false_positive=0,
        true_negative=0,
        false_negative=0,
        accuracy=0.0,
        error_rate=0.0,
        precision=0.0,
        recall=0.0,
        f1=0.0,
        observed_label_accuracy=0.0,
        observed_label_f1=0.0,
        unsafe_acceptance_rate=0.0,
        false_positive_rate=0.0,
        false_negative_rate=0.0,
        technical_failure_rate=1.0,
        rejection_rate=0.0,
        high_corruption_unsafe_acceptance_rate=0.0,
    )
