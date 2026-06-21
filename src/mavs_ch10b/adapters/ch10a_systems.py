from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mavs_ch10b.adapters.ch10a_artifacts import REQUIRED_SYSTEM_IDS
from mavs_ch10b.adapters.ch10a_source import Chapter10ASource, ensure_ch10a_importable
from mavs_ch10b.verification.hash_utils import console, read_json


@dataclass(frozen=True)
class SystemRunBundle:
    dataset_id: str
    split: str
    system_id: str
    rows: int
    trace_rows: int
    probabilities: Any
    decisions: Any
    labels: Any
    row_ids: Any


def load_frozen_manifest(source: Chapter10ASource) -> dict[str, Any]:
    path = source.repo_root / "results" / "system_fits" / "phase3_system_fit_manifest.json"
    manifest = read_json(path)
    # Phase 1 console.log: records Chapter 10A frozen system manifest loading.
    console.log("phase1.ch10a_systems.frozen_manifest_loaded", path=str(path), datasets=len(manifest.get("datasets", {})))
    return manifest


def load_specialist_bundle(source: Chapter10ASource, dataset_id: str, split: str) -> Any:
    ensure_ch10a_importable(source)
    from mavs_ch10a.systems.base import DEFAULT_SPECIALIST_ORDER, load_specialist_output_bundle

    bundle = load_specialist_output_bundle(source.repo_root, dataset_id, split, DEFAULT_SPECIALIST_ORDER)
    # Phase 1 console.log: records Chapter 10A specialist-output bundle loading.
    console.log(
        "phase1.ch10a_systems.specialist_bundle_loaded",
        dataset_id=dataset_id,
        split=split,
        rows=int(len(bundle.labels)),
        specialists=list(bundle.model_ids),
    )
    return bundle


def build_comparison_systems(source: Chapter10ASource, dataset_id: str, frozen_manifest: dict[str, Any]) -> tuple[Any, ...]:
    ensure_ch10a_importable(source)
    from mavs_ch10a.config import load_yaml
    from mavs_ch10a.systems.mean_ensemble import MeanEnsembleSystem
    from mavs_ch10a.systems.pure_mavs_gc import PureMAVSGCSystem
    from mavs_ch10a.systems.single_model import SingleModelSystem
    from mavs_ch10a.systems.static_weighted import StaticWeightedEnsembleSystem
    from mavs_ch10a.systems.veto_mavs import VetoMAVSSystem

    configs = {name: load_yaml(Path(path)) for name, path in frozen_manifest["configs"].items()}
    dataset_manifest = frozen_manifest["datasets"][dataset_id]
    systems = (
        SingleModelSystem(configs["single_model"], dataset_manifest["selected_single_model"]),
        MeanEnsembleSystem(configs["mean_ensemble"]),
        StaticWeightedEnsembleSystem(configs["static_weighted_ensemble"], dataset_manifest["static_weight_fit"]["weights"]),
        VetoMAVSSystem(configs["veto_mavs"], configs["governance_defaults"]),
        PureMAVSGCSystem(configs["pure_mavs_gc"], configs["governance_defaults"]),
    )
    system_ids = tuple(system.system_id for system in systems)
    if system_ids != REQUIRED_SYSTEM_IDS:
        raise ValueError(f"Unexpected system order: {system_ids}")
    # Phase 1 console.log: records construction of frozen Chapter 10A comparison systems.
    console.log("phase1.ch10a_systems.comparison_systems_built", dataset_id=dataset_id, systems=list(system_ids))
    return systems


def run_system(system: Any, bundle: Any) -> SystemRunBundle:
    output = system.run(bundle)
    result = SystemRunBundle(
        dataset_id=bundle.dataset_id,
        split=bundle.split,
        system_id=output.system_id,
        rows=int(len(output.decisions)),
        trace_rows=int(len(output.traces)),
        probabilities=output.probabilities,
        decisions=output.decisions,
        labels=bundle.labels,
        row_ids=bundle.row_ids,
    )
    # Phase 1 console.log: records one frozen Chapter 10A system execution.
    console.log(
        "phase1.ch10a_systems.system_executed",
        dataset_id=result.dataset_id,
        split=result.split,
        system_id=result.system_id,
        rows=result.rows,
        trace_rows=result.trace_rows,
    )
    return result

