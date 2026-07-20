"""Unit tests for HK industry ingest scope and coverage helpers."""

from __future__ import annotations

from rag.industry_hk.ingestion import is_noise_section, should_accept_section


def test_noise_section_detection() -> None:
    assert is_noise_section({"title": "Front Matter", "section_id": "x_front_matter"})
    assert is_noise_section({"title": "Table of Contents", "section_id": "toc"})
    assert not is_noise_section(
        {"title": "4.2.3 WIP Gateway", "section_id": "cicbims_2024_4_2_3"}
    )


def test_high_scope_filters_normal() -> None:
    ok, reason = should_accept_section(
        {"title": "Naming", "priority": "normal"}, ingest_scope="high"
    )
    assert not ok
    assert reason == "priority_normal_skipped"


def test_substantive_keeps_normal_body() -> None:
    ok, reason = should_accept_section(
        {"title": "LOD-I Requirements", "priority": "normal"},
        ingest_scope="substantive",
    )
    assert ok
    assert reason is None


def test_substantive_drops_noise() -> None:
    ok, reason = should_accept_section(
        {"title": "Acknowledgements", "priority": "normal"},
        ingest_scope="substantive",
    )
    assert not ok
    assert reason == "noise_section_skipped"


def test_substantive_defers_software_guides() -> None:
    ok, reason = should_accept_section(
        {
            "title": "Revit Guide",
            "priority": "normal",
            "authority_type": "software_guide",
        },
        ingest_scope="substantive",
    )
    assert not ok
    assert reason == "software_guide_deferred"
