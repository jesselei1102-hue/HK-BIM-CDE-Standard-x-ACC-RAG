"""香港 CDE 行业知识库路径常量。"""

from __future__ import annotations

from pathlib import Path

from rag.config import PROJECT_ROOT

from .source_registry import (  # noqa: E402
    HK_SOURCES_DIR,
    pdf_extract_specs,
    template_extract_specs,
)

HK_KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge" / "industry" / "hk_cde"
HK_CORPUS_DIR = HK_KNOWLEDGE_DIR / "corpus"
HK_RESEARCH_DIR = HK_KNOWLEDGE_DIR / "research"
HK_TEMPLATES_DIR = HK_CORPUS_DIR / "templates"
HK_TOC_OVERRIDES_DIR = HK_RESEARCH_DIR / "toc_overrides"
HK_QUERY_KB_PATH = HK_KNOWLEDGE_DIR / "query_kb.jsonl"
HK_SECTIONS_INDEX_PATH = HK_RESEARCH_DIR / "sections_index.jsonl"
HK_PRIORITY_SECTIONS_PATH = HK_RESEARCH_DIR / "priority_sections.json"
HK_SOURCES_MANIFEST_PATH = HK_RESEARCH_DIR / "sources_manifest.json"
HK_SOURCE_INTAKE_REPORT_PATH = HK_RESEARCH_DIR / "source_intake_report.json"
HK_PAGE_LEDGER_PATH = HK_RESEARCH_DIR / "page_ledger.jsonl"
HK_OUTLINE_MAP_PATH = HK_RESEARCH_DIR / "outline_map.json"
HK_EXTRACT_REPORT_PATH = HK_RESEARCH_DIR / "extract_report.json"

HK_RAG_DATA_DIR = PROJECT_ROOT / ".rag_data" / "industry_hk_cde"
HK_CHROMA_DIR = HK_RAG_DATA_DIR / "chroma"
HK_CHUNKS_PATH = HK_RAG_DATA_DIR / "chunks.jsonl"
HK_MANIFEST_PATH = HK_RAG_DATA_DIR / "manifest.json"
HK_KB_CHROMA_DIR = HK_RAG_DATA_DIR / "kb_chroma"
HK_KB_MANIFEST_PATH = HK_RAG_DATA_DIR / "kb_route_manifest.json"

HK_COLLECTION_NAME = "industry_hk_cde"
HK_KB_COLLECTION_NAME = "industry_hk_cde_route"

# Legacy names kept for extract/validate scripts.
PDF_SOURCES = tuple(pdf_extract_specs())
TEMPLATE_SOURCES = tuple(template_extract_specs())


def section_url(doc_id: str, section_id: str) -> str:
    return f"hk_cde://{doc_id}/{section_id}"


def storage_paths(data_dir: Path | None = None) -> dict[str, Path]:
    """Resolve chunk/chroma/manifest paths from a data directory override."""
    root = data_dir or HK_RAG_DATA_DIR
    return {
        "data_dir": root,
        "chroma_dir": root / "chroma",
        "chunks_path": root / "chunks.jsonl",
        "manifest_path": root / "manifest.json",
        "kb_chroma_dir": root / "kb_chroma",
        "kb_manifest_path": root / "kb_route_manifest.json",
    }
