"""Unit tests for hybrid answer validation."""

from __future__ import annotations

from rag.orchestrator.merge import MergedContexts, TrackedChunk, merge_triple_contexts
from rag.orchestrator.validate import validate_hybrid_answer
from rag.retrieval import RetrievedChunk


def _chunk(title: str, url: str, text: str, product: str = "x") -> RetrievedChunk:
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
        token_count=10,
        text=text,
        score=1.0,
        vector_similarity=0.9,
    )


def test_validate_hybrid_accepts_correct_track_citations() -> None:
    hk = _chunk("WIP", "hk_cde://cicbims/wip", "WIP Shared Published", "hk_cde")
    pb = _chunk("WIP tree", "playbook://wip", "01_WIP folders", "playbook")
    docs = _chunk(
        "Organize Files",
        "https://help.autodesk.com/view/DOCS/ENU/?guid=Organize_Files",
        "Create folders in Files tool",
        "docs",
    )
    merged = merge_triple_contexts(
        docs_chunks=[docs],
        industry_chunks=[hk],
        playbook_chunks=[pb],
    )
    answer = (
        "## Standards Requirements\nUse WIP/Shared/Published [1].\n\n"
        "## Implementation Guidance\nFollow 01_WIP tree [2].\n\n"
        "## Product Operations\nCreate folders in Docs [3].\n\n"
        "## Alignment and Gaps\nStandards and product align; remaining gap is BEP discipline [1][2][3]."
    )
    result = validate_hybrid_answer(answer, merged, capability="folder")
    assert result.ok or not result.hard_issues
    assert not any(i.severity == "hard" for i in result.issues)


def test_validate_hybrid_flags_cross_track_citation() -> None:
    hk = _chunk("WIP", "hk_cde://cicbims/wip", "WIP Shared Published", "hk_cde")
    pb = _chunk("WIP tree", "playbook://wip", "01_WIP folders", "playbook")
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
    # Standards cites Docs index 3.
    answer = (
        "## Standards Requirements\nFolders [3].\n\n"
        "## Implementation Guidance\nTree [2].\n\n"
        "## Product Operations\nCreate [3].\n\n"
        "## Alignment and Gaps\nGap noted [1][3]."
    )
    result = validate_hybrid_answer(answer, merged)
    assert any(i.code == "standards_wrong_track" for i in result.issues)


def test_validate_hybrid_soft_authority_guard() -> None:
    hk = _chunk(
        "ZCP case",
        "hk_cde://cic_zcp/bep",
        "authority_type: case_study\nnormative_weight: reference\nBIM IP example",
        "hk_cde",
    )
    docs = _chunk(
        "Reviews",
        "https://help.autodesk.com/view/DOCS/ENU/?guid=Reviews",
        "Create review",
        "docs",
    )
    merged = merge_triple_contexts(
        docs_chunks=[docs],
        industry_chunks=[hk],
        playbook_chunks=[],
    )
    answer = (
        "## Standards Requirements\nThis is a mandatory binding standard for all projects [1].\n\n"
        "## Product Operations\nCreate a review [2].\n\n"
        "## Alignment and Gaps\nCase study is reference only [1][2]."
    )
    result = validate_hybrid_answer(answer, merged)
    assert any(i.code == "authority_overclaim" for i in result.issues) or any(
        "mandatory" in (i.message or "").lower() or i.code.startswith("authority")
        for i in result.issues
    )
