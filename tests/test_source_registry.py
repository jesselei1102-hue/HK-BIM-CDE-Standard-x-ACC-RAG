"""Source registry inventory tests."""

from __future__ import annotations

import pytest

from rag.industry_hk.source_registry import (
    inventory_sources,
    pdf_extract_specs,
    resolve_spec,
)


def test_registry_resolves_relocated_general_pdf() -> None:
    spec = resolve_spec("cicbims_2024")
    assert spec is not None
    if not spec.path.is_file():
        pytest.skip("requires local HK Standard PDFs")
    assert spec.path.is_file()
    assert "CIC BIM Standard" in str(spec.path)


def test_registry_includes_new_discipline_standards() -> None:
    ids = {item["doc_id"] for item in pdf_extract_specs()}
    assert "cic_mep_2021" in ids
    assert "cic_uu_2021" in ids
    assert "cic_statutory_plans_2020" in ids
    assert "cic_dictionary_2024" in ids


def test_inventory_has_no_missing_or_duplicates() -> None:
    report = inventory_sources()
    if report["counts"]["missing"] > 0:
        pytest.skip("requires complete local HK source inventory")
    assert report["counts"]["missing"] == 0
    assert report["counts"]["duplicates"] == 0
    assert report["counts"]["extractable_pdfs"] >= 10
