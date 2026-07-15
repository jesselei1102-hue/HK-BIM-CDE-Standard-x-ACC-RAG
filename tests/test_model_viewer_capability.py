"""model_viewer capability：分类、Docs 钉选、噪声预过滤。"""

from __future__ import annotations

from pathlib import Path

from rag.orchestrator.classify import classify_intent, detect_capability
from rag.orchestrator.chunk_pin import (
    DOCS_MODEL_BROWSER_GUID,
    load_docs_model_viewer_chunks,
)
from rag.orchestrator.merge import MergedContexts, TrackedChunk, merge_triple_contexts
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


def test_detect_model_viewer_capability() -> None:
    q = "在 ACC 里如何查看并过滤 BIM 模型属性，并对照香港 BIM 要求做审核？"
    cap = detect_capability(q)
    assert cap is not None
    assert cap.key == "model_viewer"
    decision = classify_intent(q)
    assert decision.track == "hybrid"
    assert decision.capability == "model_viewer"
    assert "Model Browser" in (decision.product_query or "")


def test_load_model_browser_pin_from_chunks() -> None:
    path = Path(".rag_data/chunks.jsonl")
    if not path.is_file():
        return
    found = load_docs_model_viewer_chunks(path, limit=2)
    assert found
    assert any(DOCS_MODEL_BROWSER_GUID in c.source_url for c in found)
    assert not any("Viewer_Settings_Files_PDF" in c.source_url for c in found)
    if len(found) >= 2:
        assert "guid=Viewer_Settings_Files" in found[1].source_url
        assert "PDF" not in found[1].title


def test_prefilter_keeps_model_browser_drops_power_bi() -> None:
    browser = _chunk(
        title="Model Browser",
        url=f"https://help.autodesk.com/view/DOCS/ENU/?guid={DOCS_MODEL_BROWSER_GUID}",
        text="Filter RVT IFC object properties in Model Browser",
        chunk_id="mb",
    )
    power_bi = _chunk(
        title="Power BI Templates",
        url="https://help.autodesk.com/view/DOCS/ENU/?guid=Power_BI_Templates",
        text="Power BI templates overview",
        chunk_id="pbi",
    )
    about = _chunk(
        title="About Autodesk Construction Cloud Collaborate",
        url="https://help.autodesk.com/view/DOCS/ENU/?guid=About_Autodesk_Construction_Cloud",
        text="Collaborate overview",
        chunk_id="about",
    )
    merged = merge_triple_contexts(
        docs_chunks=[power_bi, about, browser],
        industry_chunks=[],
        playbook_chunks=[],
        docs_top_k=3,
        industry_top_k=0,
        playbook_top_k=0,
        maximum_context_tokens=10_000,
    )
    filtered, drops = prefilter_docs_for_capability(merged, "model_viewer")
    titles = {t.chunk.title for t in filtered.tracked if t.track == "docs"}
    assert "Model Browser" in titles
    assert "Power BI Templates" not in titles
    assert drops
