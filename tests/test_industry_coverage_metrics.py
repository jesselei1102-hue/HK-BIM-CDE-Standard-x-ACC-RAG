"""Coverage metric helpers for HK industry ingest."""

from __future__ import annotations

from types import SimpleNamespace

from scripts.ingest_industry_hk_cde import _coverage_from_documents


def test_coverage_counts_same_page_across_docs(tmp_path) -> None:
    corpus = tmp_path / "corpus"
    a = corpus / "doc_a"
    b = corpus / "doc_b"
    a.mkdir(parents=True)
    b.mkdir(parents=True)
    path_a = a / "s1.md"
    path_b = b / "s1.md"
    path_a.write_text(
        "---\ndoc_id: doc_a\npage_start: 1\npage_end: 2\ntitle: A\n---\n\nbody text enough\n",
        encoding="utf-8",
    )
    path_b.write_text(
        "---\ndoc_id: doc_b\npage_start: 1\npage_end: 1\ntitle: B\n---\n\nbody text enough\n",
        encoding="utf-8",
    )
    docs = [
        SimpleNamespace(source_file=str(path_a), page_index=1),
        SimpleNamespace(source_file=str(path_b), page_index=1),
    ]
    coverage = _coverage_from_documents(docs, corpus)
    assert coverage["accepted_sections"] == 2
    assert coverage["total_sections"] == 2
    assert coverage["accepted_page_keys"] == 3
    assert coverage["total_page_keys"] == 3
    assert coverage["page_range_ingest_pct"] == 100.0
