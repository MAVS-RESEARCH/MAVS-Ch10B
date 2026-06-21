from __future__ import annotations

from pathlib import Path

from mavs_ch10b.adapters.ch10a_artifacts import validate_governance_trace_schema
from mavs_ch10b.adapters.ch10a_source import locate_ch10a_source


def test_ch10a_governance_trace_schema_sample_is_compatible() -> None:
    source = locate_ch10a_source(Path.cwd())
    result = validate_governance_trace_schema(source.repo_root, max_records_per_file=5)
    assert result["checked_records"] == 80
    assert result["failures"] == []

