"""Unit tests for structured hybrid compose."""

from __future__ import annotations

from rag.orchestrator.merge import merge_triple_contexts
from rag.orchestrator.structured_compose import (
    compose_folder_hybrid,
    try_compose_structured_hybrid,
)
from rag.retrieval import RetrievedChunk


def _chunk(title: str, url: str, text: str, product: str) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=url,
        title=title,
        source_url=url,
        source_file=f"{title}.md",
        page_index=0,
        line_start=1,
        product=product,
        chunk_index=0,
        chunk_count=1,
        token_count=20,
        text=text,
        score=1.0,
        vector_similarity=0.9,
    )


def test_compose_folder_hybrid_requires_wip_playbook() -> None:
    hk = _chunk(
        "CDE states",
        "hk_cde://cicbims/cde",
        "WIP Shared Published Archive",
        "hk_cde",
    )
    pb = _chunk(
        "WIP folders",
        "playbook://01_wip",
        "01_WIP\n- Architecture\n- Structure\n2_wip tree",
        "playbook",
    )
    docs = _chunk(
        "Organize Files",
        "https://help.autodesk.com/view/DOCS/ENU/?guid=Organize_Files",
        "Create a folder under Files",
        "docs",
    )
    merged = merge_triple_contexts(
        docs_chunks=[docs],
        industry_chunks=[hk],
        playbook_chunks=[pb],
    )
    text = compose_folder_hybrid(merged, lang="en")
    assert text is not None
    assert "## Standards" in text or "Standards" in text
    assert "[1]" in text and "[2]" in text and "[3]" in text


def test_try_compose_structured_hybrid_folder_capability() -> None:
    hk = _chunk(
        "CDE states",
        "hk_cde://cicbims/cde",
        "WIP Shared Published",
        "hk_cde",
    )
    pb = _chunk(
        "WIP folders",
        "playbook://2_wip",
        "01_WIP discipline folders tree",
        "playbook",
    )
    docs = _chunk(
        "Organize Files",
        "https://help.autodesk.com/view/DOCS/ENU/?guid=Organize_Files",
        "Create folders",
        "docs",
    )
    merged = merge_triple_contexts(
        docs_chunks=[docs],
        industry_chunks=[hk],
        playbook_chunks=[pb],
    )
    text = try_compose_structured_hybrid(
        merged,
        "folder",
        question="How should HK CDE folders be set up in ACC?",
        answer_lang="en",
    )
    assert text is not None
    assert "WIP" in text or "folder" in text.lower()
