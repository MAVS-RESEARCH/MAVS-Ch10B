from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path
from typing import Any

import numpy as np

from mavs_ch10b.adapters.ch10a_artifacts import CH10A_TRACE_FIELDS, REQUIRED_SPECIALIST_IDS
from mavs_ch10b.corruptions.base import array_hash
from mavs_ch10b.stress.system_executor import PreparedCorruptionBundle
from mavs_ch10b.verification.hash_utils import console, hash_file, hash_json


STRESS_TRACE_FIELDS: tuple[str, ...] = (
    "corruption_family",
    "corruption_id",
    "corruption_level",
    "corruption_seed",
    "corruption_target_space",
    "corruption_config_hash",
    "corruption_manifest_hash",
    "y_clean",
    "y_observed",
    "input_hash_clean",
    "input_hash_corrupted",
    "score_hash_clean",
    "score_hash_corrupted",
    "failed_specialists",
    "feature_mask_hash",
    "distribution_shift_descriptor",
)


def write_prediction_output(path: Path, output: Any, prepared: PreparedCorruptionBundle) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    arrays = {
        "row_ids": np.asarray(prepared.corruption_output.row_ids),
        "probabilities": np.asarray(output.probabilities, dtype=np.float64),
        "decisions": np.asarray(output.decisions, dtype=np.int8),
        "y_clean": np.asarray(prepared.corruption_output.y_clean, dtype=np.int8),
        "y_observed": np.asarray(prepared.corruption_output.y_observed, dtype=np.int8),
    }
    # Phase 3 console.log: records prediction artifact persistence dispatch.
    console.log("phase3.trace_writer.prediction_write_start", path=str(path), system_id=output.system_id, rows=int(arrays["row_ids"].shape[0]))
    write_npz_deterministic(path, arrays)
    record = {
        "prediction_path": str(path),
        "prediction_sha256": hash_file(path),
        "prediction_payload_hash": hash_json({key: array_hash(value) for key, value in arrays.items()}),
        "prediction_rows": int(arrays["row_ids"].shape[0]),
    }
    # Phase 3 console.log: records prediction artifact persistence completion.
    console.log("phase3.trace_writer.prediction_write_complete", path=str(path), sha256=record["prediction_sha256"], rows=record["prediction_rows"])
    return record


def write_governance_traces(path: Path, output: Any, prepared: PreparedCorruptionBundle) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    required_specialists = set(REQUIRED_SPECIALIST_IDS)
    # Phase 3 console.log: records governance trace artifact persistence dispatch.
    console.log("phase3.trace_writer.trace_write_start", path=str(path), system_id=output.system_id, traces=len(output.traces))
    arrays, metadata = columnar_trace_payload(output, prepared)
    if set(metadata["specialist_ids"]) != required_specialists:
        raise ValueError(f"Specialist coverage failure in trace: {metadata['specialist_ids']}")
    metadata["metadata_hash"] = hash_json(metadata)
    arrays["metadata_json"] = np.asarray(json.dumps(metadata, sort_keys=True))
    write_npz_deterministic(path, arrays)
    row_count = int(arrays["x_id"].shape[0])
    record = {
        "trace_path": str(path),
        "trace_sha256": hash_file(path),
        "trace_rows": row_count,
        "specialist_count": len(REQUIRED_SPECIALIST_IDS),
        "trace_format": "columnar_npz",
        "trace_schema_hash": metadata["metadata_hash"],
    }
    # Phase 3 console.log: records governance trace artifact persistence completion.
    console.log("phase3.trace_writer.trace_write_complete", path=str(path), sha256=record["trace_sha256"], rows=row_count)
    return record


def columnar_trace_payload(output: Any, prepared: PreparedCorruptionBundle) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    if not output.traces:
        raise ValueError(f"Governance output has no traces: {output.system_id}")
    first = output.traces[0]
    missing = [field for field in CH10A_TRACE_FIELDS if field not in first]
    if missing:
        raise ValueError(f"Governance trace missing inherited fields: {missing}")
    specialist_ids = list(first["specialist_ids"])
    z_fields = sorted(first["z"])
    rows = len(output.traces)
    arrays: dict[str, np.ndarray] = {
        "x_id": np.asarray([trace["x_id"] for trace in output.traces], dtype=np.int64),
        "s": np.asarray([[trace["s"][specialist_id] for specialist_id in specialist_ids] for trace in output.traces], dtype=np.float64),
        "r": np.asarray([[trace["r"][specialist_id] for specialist_id in specialist_ids] for trace in output.traces], dtype=np.float64),
        "z": np.asarray([[trace["z"][field] for field in z_fields] for trace in output.traces], dtype=np.float64),
        "a": np.asarray([trace["a"] for trace in output.traces], dtype=np.float64),
        "w": np.asarray([[trace["w"][specialist_id] for specialist_id in specialist_ids] for trace in output.traces], dtype=np.float64),
        "m": np.asarray([trace["m"] for trace in output.traces], dtype=np.float64),
        "theta": np.asarray([trace["theta"] for trace in output.traces], dtype=np.float64),
        "R": np.asarray([trace["R"] for trace in output.traces], dtype=np.float64),
        "hard_veto": np.asarray([trace["hard_veto"] for trace in output.traces], dtype=np.bool_),
        "decision": np.asarray([trace["decision"] for trace in output.traces], dtype=np.int8),
        "label": np.asarray([trace["label"] for trace in output.traces], dtype=np.int8),
        "y_clean": np.asarray(prepared.corruption_output.y_clean, dtype=np.int8),
        "y_observed": np.asarray(prepared.corruption_output.y_observed, dtype=np.int8),
        "trace_hash": np.asarray([str(trace["trace_hash"]) for trace in output.traces]),
    }
    metadata = {
        "format": "columnar_npz",
        "schema_version": "1.0",
        "rows": rows,
        "fields": list(CH10A_TRACE_FIELDS) + list(STRESS_TRACE_FIELDS),
        "dataset_id": prepared.definition.dataset_id,
        "split": prepared.definition.split,
        "system_id": output.system_id,
        "specialist_ids": specialist_ids,
        "z_fields": z_fields,
        "config_hash": str(first["config_hash"]),
        "checkpoint_hashes": dict(first["checkpoint_hashes"]),
        "corruption_family": prepared.definition.corruption_family,
        "corruption_id": prepared.definition.corruption_id,
        "corruption_level": prepared.definition.level,
        "corruption_seed": prepared.definition.seed,
        "corruption_target_space": prepared.definition.target_space,
        "corruption_config_hash": prepared.definition.corruption_config_hash,
        "corruption_manifest_hash": prepared.metadata["applied_corruption_manifest_hash"],
        "input_hash_clean": prepared.metadata["input_hash_clean"],
        "input_hash_corrupted": prepared.metadata["input_hash_corrupted"],
        "score_hash_clean": prepared.metadata["score_hash_clean"],
        "score_hash_corrupted": prepared.metadata["score_hash_corrupted"],
        "failed_specialists": prepared.metadata["failed_specialists"],
        "feature_mask_hash": prepared.metadata["feature_mask_hash"],
        "distribution_shift_descriptor": prepared.metadata["distribution_shift_descriptor"],
    }
    # Phase 3 console.log: records conversion of row governance traces into columnar stress traces.
    console.log("phase3.trace_writer.trace_columnar_payload_built", system_id=output.system_id, rows=rows, fields=len(metadata["fields"]))
    return arrays, metadata


def enrich_trace_record(trace: dict[str, Any], row_index: int, prepared: PreparedCorruptionBundle) -> dict[str, Any]:
    missing = [field for field in CH10A_TRACE_FIELDS if field not in trace]
    if missing:
        raise ValueError(f"Governance trace missing inherited fields: {missing}")
    output = prepared.corruption_output
    metadata = prepared.metadata
    payload = dict(trace)
    inherited_hash = payload.pop("trace_hash", None)
    payload["inherited_trace_hash"] = inherited_hash
    payload.update(
        {
            "corruption_family": prepared.definition.corruption_family,
            "corruption_id": prepared.definition.corruption_id,
            "corruption_level": prepared.definition.level,
            "corruption_seed": prepared.definition.seed,
            "corruption_target_space": prepared.definition.target_space,
            "corruption_config_hash": prepared.definition.corruption_config_hash,
            "corruption_manifest_hash": metadata["applied_corruption_manifest_hash"],
            "y_clean": int(output.y_clean[row_index]),
            "y_observed": int(output.y_observed[row_index]),
            "input_hash_clean": metadata["input_hash_clean"],
            "input_hash_corrupted": metadata["input_hash_corrupted"],
            "score_hash_clean": metadata["score_hash_clean"],
            "score_hash_corrupted": metadata["score_hash_corrupted"],
            "failed_specialists": metadata["failed_specialists"],
            "feature_mask_hash": metadata["feature_mask_hash"],
            "distribution_shift_descriptor": metadata["distribution_shift_descriptor"],
        }
    )
    payload["trace_hash"] = hash_json(payload)
    return payload


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        raise ValueError(f"No records to write: {path}")
    fieldnames = list(records[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    # Phase 3 console.log: records Phase 3 CSV index persistence.
    console.log("phase3.trace_writer.csv_written", path=str(path), rows=len(records))


def write_npz_deterministic(path: Path, arrays: dict[str, np.ndarray]) -> None:
    with zipfile.ZipFile(path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name in sorted(arrays):
            buffer = io.BytesIO()
            np.save(buffer, arrays[name], allow_pickle=False)
            info = zipfile.ZipInfo(f"{name}.npy", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, buffer.getvalue())
