from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from mavs_ch10b.adapters.ch10a_source import Chapter10ASource, ensure_ch10a_importable
from mavs_ch10b.adapters.ch10a_systems import load_specialist_bundle
from mavs_ch10b.corruptions.base import array_hash
from mavs_ch10b.verification.hash_utils import console, hash_file


@dataclass(frozen=True)
class CleanBenchmarkBundle:
    dataset_id: str
    split: str
    features: np.ndarray
    feature_names: tuple[str, ...]
    specialist_bundle: Any
    feature_hash: str


class StressCache:
    def __init__(self, source: Chapter10ASource):
        self.source = source
        self._clean_bundles: dict[tuple[str, str], CleanBenchmarkBundle] = {}
        self._specialists: dict[tuple[str, str], Any] = {}
        self._prediction_cache: dict[tuple[str, str], tuple[np.ndarray, np.ndarray, dict[str, str]]] = {}

    def clean_benchmark_bundle(self, dataset_id: str, split: str) -> CleanBenchmarkBundle:
        key = (dataset_id, split)
        if key in self._clean_bundles:
            # Phase 3 console.log: records cache reuse for a clean benchmark bundle.
            console.log("phase3.cache.clean_bundle_reused", dataset_id=dataset_id, split=split)
            return self._clean_bundles[key]
        # Phase 3 console.log: records cache loading for a clean benchmark bundle.
        console.log("phase3.cache.clean_bundle_load_start", dataset_id=dataset_id, split=split)
        manifest = json.loads((self.source.repo_root / "datasets" / "manifests" / f"{dataset_id}.json").read_text(encoding="utf-8"))
        processed_path = Path(manifest["artifacts"]["processed_splits"][split])
        loaded = np.load(processed_path)
        features = np.asarray(loaded["X"], dtype=np.float64)
        feature_names = self._feature_names(manifest, features.shape[1])
        specialist_bundle = load_specialist_bundle(self.source, dataset_id, split)
        clean = CleanBenchmarkBundle(
            dataset_id=dataset_id,
            split=split,
            features=features,
            feature_names=feature_names,
            specialist_bundle=specialist_bundle,
            feature_hash=array_hash(features),
        )
        self._clean_bundles[key] = clean
        # Phase 3 console.log: records cache completion for a clean benchmark bundle.
        console.log(
            "phase3.cache.clean_bundle_loaded",
            dataset_id=dataset_id,
            split=split,
            rows=int(features.shape[0]),
            features=int(features.shape[1]),
            feature_hash=clean.feature_hash,
        )
        return clean

    def predict_specialists(self, dataset_id: str, features: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict[str, str]]:
        ensure_ch10a_importable(self.source)
        from mavs_ch10a.systems.base import DEFAULT_SPECIALIST_ORDER

        feature_hash = array_hash(features)
        cache_key = (dataset_id, feature_hash)
        if cache_key in self._prediction_cache:
            probabilities, supports, checkpoint_hashes = self._prediction_cache[cache_key]
            # Phase 3 console.log: records specialist prediction cache reuse for a repeated corrupted feature matrix.
            console.log("phase3.cache.specialist_prediction_reused", dataset_id=dataset_id, rows=int(features.shape[0]), feature_hash=feature_hash)
            return np.array(probabilities, copy=True), np.array(supports, copy=True), dict(checkpoint_hashes)
        probabilities: list[np.ndarray] = []
        supports: list[np.ndarray] = []
        checkpoint_hashes: dict[str, str] = {}
        # Phase 3 console.log: records specialist prediction dispatch for corrupted input features.
        console.log("phase3.cache.specialist_predict_start", dataset_id=dataset_id, rows=int(features.shape[0]), feature_hash=feature_hash)
        for specialist_id in DEFAULT_SPECIALIST_ORDER:
            specialist = self._load_specialist(dataset_id, specialist_id)
            probabilities.append(specialist.predict_proba(features)[:, 1])
            supports.append(specialist.predict_support(features))
            checkpoint_path = self.source.repo_root / "results" / "checkpoints" / f"{dataset_id}__{specialist_id}.joblib"
            metadata_path = self.source.repo_root / "results" / "checkpoints" / f"{dataset_id}__{specialist_id}.metadata.json"
            if metadata_path.exists():
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                checkpoint_hashes[specialist_id] = str(metadata.get("checkpoint_sha256", hash_file(checkpoint_path)))
            else:
                checkpoint_hashes[specialist_id] = hash_file(checkpoint_path)
        probability_matrix = np.column_stack(probabilities)
        support_matrix = np.column_stack(supports)
        self._prediction_cache[cache_key] = (np.array(probability_matrix, copy=True), np.array(support_matrix, copy=True), dict(checkpoint_hashes))
        # Phase 3 console.log: records specialist prediction completion for corrupted input features.
        console.log(
            "phase3.cache.specialist_predict_complete",
            dataset_id=dataset_id,
            rows=int(probability_matrix.shape[0]),
            specialists=int(probability_matrix.shape[1]),
            score_hash=array_hash(probability_matrix),
        )
        return probability_matrix, support_matrix, checkpoint_hashes

    def _load_specialist(self, dataset_id: str, specialist_id: str) -> Any:
        key = (dataset_id, specialist_id)
        if key in self._specialists:
            return self._specialists[key]
        ensure_ch10a_importable(self.source)
        from mavs_ch10a.models.checkpoints import load_specialist_checkpoint

        checkpoint_path = self.source.repo_root / "results" / "checkpoints" / f"{dataset_id}__{specialist_id}.joblib"
        # Phase 3 console.log: records frozen specialist checkpoint loading for corrupted-feature inference.
        console.log("phase3.cache.specialist_loaded", dataset_id=dataset_id, specialist_id=specialist_id, checkpoint_path=str(checkpoint_path))
        specialist = load_specialist_checkpoint(checkpoint_path)
        self._specialists[key] = specialist
        return specialist

    def _feature_names(self, manifest: dict[str, Any], width: int) -> tuple[str, ...]:
        path_value = manifest.get("artifacts", {}).get("feature_names_path")
        if path_value:
            path = Path(path_value)
            if path.exists():
                names = tuple(str(name) for name in json.loads(path.read_text(encoding="utf-8")))
                if len(names) == width:
                    return names
        return tuple(f"processed_feature_{index:04d}" for index in range(width))
