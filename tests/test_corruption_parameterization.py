from __future__ import annotations

from pathlib import Path

from mavs_ch10b.corruptions.grid import build_corruption_grid
from mavs_ch10b.corruptions.registry import REQUIRED_CORRUPTION_FAMILIES, build_registry


def test_every_required_corruption_family_is_registered() -> None:
    registry = build_registry(Path.cwd())
    assert tuple(registry) == REQUIRED_CORRUPTION_FAMILIES
    assert all(registry[family].target_space for family in REQUIRED_CORRUPTION_FAMILIES)


def test_grid_contains_level_zero_and_one_for_every_family() -> None:
    definitions = build_corruption_grid(Path.cwd())
    by_family: dict[str, set[float]] = {family: set() for family in REQUIRED_CORRUPTION_FAMILIES}
    for definition in definitions:
        by_family[definition.corruption_family].add(definition.level)
    for family, levels in by_family.items():
        assert 0.0 in levels, family
        assert 1.0 in levels, family

