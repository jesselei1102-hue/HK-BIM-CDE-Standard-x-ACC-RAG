"""弱能力 Docs 优先选择与校验关键词。"""

from __future__ import annotations

from pathlib import Path

from rag.orchestrator.chunk_pin import (
    DOCS_PERMISSIONS_GUID,
    DOCS_REVIEWS_CREATE_GUID,
    DOCS_TEMPLATES_DOCS_GUID,
    prefer_docs_chunks,
    prefer_docs_for_capability,
)
from rag.orchestrator.merge import merge_triple_contexts
from rag.orchestrator.validate import prefilter_docs_for_capability
from rag.retrieval import RetrievedChunk


def _chunk(
    *,
    title: str,
    url: str,
    text: str = "x",
    chunk_id: str = "c1",
) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=chunk_id,
        title=title,
        source_url=url,
        source_file="t.md",
        page_index=1,
        line_start=1,
        product="DOCS",
        chunk_index=0,
        chunk_count=1,
        token_count=10,
        text=text,
        score=1.0,
        vector_similarity=0.9,
    )


def test_prefer_docs_keeps_retrieved_as_second_source() -> None:
    preferred = [
        _chunk(
            title="Manage Folder Permissions",
            url=f"https://x/?guid={DOCS_PERMISSIONS_GUID}",
            chunk_id="perm",
        )
    ]
    retrieved = [
        _chunk(
            title="About Autodesk Docs",
            url="https://x/?guid=About_Docs",
            chunk_id="about",
        ),
        _chunk(
            title="Manage Folder Permissions",
            url=f"https://x/?guid={DOCS_PERMISSIONS_GUID}",
            chunk_id="perm",
        ),
    ]
    out = prefer_docs_chunks(preferred, retrieved, limit=2)
    assert out[0].chunk_id == "perm"
    assert out[1].chunk_id == "about"


def test_prefilter_permissions_and_project_template() -> None:
    perm = _chunk(
        title="Manage Folder Permissions",
        url=f"https://help.autodesk.com/view/DOCS/ENU/?guid={DOCS_PERMISSIONS_GUID}",
        text="Folder permissions levels",
        chunk_id="perm",
    )
    about = _chunk(
        title="About Autodesk Construction Cloud",
        url="https://help.autodesk.com/view/DOCS/ENU/?guid=About_Autodesk_Construction_Cloud",
        text="overview",
        chunk_id="about",
    )
    tmpl = _chunk(
        title="Configure Project Templates for Autodesk Docs",
        url=f"https://help.autodesk.com/view/DOCS/ENU/?guid={DOCS_TEMPLATES_DOCS_GUID}",
        text="project template",
        chunk_id="tmpl",
    )
    merged = merge_triple_contexts(
        docs_chunks=[about, perm],
        industry_chunks=[],
        playbook_chunks=[],
        docs_top_k=2,
        industry_top_k=0,
        playbook_top_k=0,
        maximum_context_tokens=10_000,
    )
    filtered, drops = prefilter_docs_for_capability(merged, "permissions")
    titles = {t.chunk.title for t in filtered.tracked if t.track == "docs"}
    assert "Manage Folder Permissions" in titles
    assert "About Autodesk Construction Cloud" not in titles
    assert drops

    merged2 = merge_triple_contexts(
        docs_chunks=[about, tmpl],
        industry_chunks=[],
        playbook_chunks=[],
        docs_top_k=2,
        industry_top_k=0,
        playbook_top_k=0,
        maximum_context_tokens=10_000,
    )
    filtered2, drops2 = prefilter_docs_for_capability(merged2, "project_template")
    titles2 = {t.chunk.title for t in filtered2.tracked if t.track == "docs"}
    assert "Configure Project Templates for Autodesk Docs" in titles2
    assert drops2


def test_prefer_docs_for_capability_from_chunks_file() -> None:
    path = Path(".rag_data/chunks.jsonl")
    if not path.is_file():
        return
    weak = [
        _chunk(
            title="Power BI Templates",
            url="https://help.autodesk.com/view/DOCS/ENU/?guid=Power_BI_Templates",
            chunk_id="pbi",
        )
    ]
    out = prefer_docs_for_capability(
        "workflow",
        weak,
        chunks_path=path,
        limit=2,
    )
    assert any(DOCS_REVIEWS_CREATE_GUID in c.source_url for c in out)
    assert out[0].chunk_id != "pbi" or DOCS_REVIEWS_CREATE_GUID in out[0].source_url
