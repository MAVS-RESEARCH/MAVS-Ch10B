from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from mavs_ch10b.corruptions.adversarial_confidence_inflation import AdversarialConfidenceInflationCorruption
from mavs_ch10b.corruptions.base import Corruption
from mavs_ch10b.corruptions.confidence_distortion import ConfidenceDistortionCorruption
from mavs_ch10b.corruptions.distribution_shift import DistributionShiftCorruption
from mavs_ch10b.corruptions.feature_noise import FeatureNoiseCorruption
from mavs_ch10b.corruptions.label_noise import LabelNoiseCorruption
from mavs_ch10b.corruptions.missing_features import MissingFeaturesCorruption
from mavs_ch10b.corruptions.random_feature_deletion import RandomFeatureDeletionCorruption
from mavs_ch10b.corruptions.specialist_failure import SpecialistFailureCorruption
from mavs_ch10b.corruptions.synthetic_sensor_failure import SyntheticSensorFailureCorruption
from mavs_ch10b.verification.hash_utils import console


REQUIRED_CORRUPTION_FAMILIES: tuple[str, ...] = (
    "feature_noise",
    "missing_features",
    "random_feature_deletion",
    "label_noise",
    "confidence_distortion",
    "adversarial_confidence_inflation",
    "distribution_shift",
    "synthetic_sensor_failure",
    "specialist_failure",
)

CORRUPTION_CLASSES: dict[str, type[Corruption]] = {
    "feature_noise": FeatureNoiseCorruption,
    "missing_features": MissingFeaturesCorruption,
    "random_feature_deletion": RandomFeatureDeletionCorruption,
    "label_noise": LabelNoiseCorruption,
    "confidence_distortion": ConfidenceDistortionCorruption,
    "adversarial_confidence_inflation": AdversarialConfidenceInflationCorruption,
    "distribution_shift": DistributionShiftCorruption,
    "synthetic_sensor_failure": SyntheticSensorFailureCorruption,
    "specialist_failure": SpecialistFailureCorruption,
}


def build_registry(repo_root: Path) -> dict[str, Corruption]:
    registry: dict[str, Corruption] = {}
    for family in REQUIRED_CORRUPTION_FAMILIES:
        config_path = repo_root / "configs" / "corruptions" / f"{family}.yaml"
        config = load_corruption_config(config_path)
        if config["corruption_family"] != family:
            raise ValueError(f"Corruption config family mismatch for {family}: {config['corruption_family']}")
        registry[family] = CORRUPTION_CLASSES[family](config)
    missing = set(REQUIRED_CORRUPTION_FAMILIES) - set(registry)
    if missing:
        raise ValueError(f"Missing required corruption families: {sorted(missing)}")
    # Phase 2 console.log: records corruption registry construction.
    console.log("phase2.corruption.registry_built", families=list(registry))
    return registry


def load_corruption_config(path: Path) -> dict[str, Any]:
    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    required = {"corruption_family", "target_space", "parameters"}
    missing = required - set(config)
    if missing:
        raise ValueError(f"Corruption config missing keys {sorted(missing)}: {path}")
    # Phase 2 console.log: records corruption configuration loading.
    console.log("phase2.corruption.config_loaded", path=str(path), family=config["corruption_family"])
    return config

