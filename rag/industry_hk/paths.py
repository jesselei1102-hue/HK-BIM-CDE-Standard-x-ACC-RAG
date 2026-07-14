"""香港 CDE 行业知识库路径常量。"""

from __future__ import annotations

from pathlib import Path

from rag.config import PROJECT_ROOT

HK_SOURCES_DIR = PROJECT_ROOT / "output" / "HK Standard"
HK_KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge" / "industry" / "hk_cde"
HK_CORPUS_DIR = HK_KNOWLEDGE_DIR / "corpus"
HK_RESEARCH_DIR = HK_KNOWLEDGE_DIR / "research"
HK_TEMPLATES_DIR = HK_CORPUS_DIR / "templates"
HK_TOC_OVERRIDES_DIR = HK_RESEARCH_DIR / "toc_overrides"
HK_QUERY_KB_PATH = HK_KNOWLEDGE_DIR / "query_kb.jsonl"
HK_SECTIONS_INDEX_PATH = HK_RESEARCH_DIR / "sections_index.jsonl"
HK_PRIORITY_SECTIONS_PATH = HK_RESEARCH_DIR / "priority_sections.json"
HK_SOURCES_MANIFEST_PATH = HK_RESEARCH_DIR / "sources_manifest.json"
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

PDF_SOURCES = (
    {
        "doc_id": "cicbims_2024",
        "path": HK_SOURCES_DIR
        / "CIC BIM Standards General 2024"
        / "CIC BIM Standards General (Version 2024).pdf",
        "authority_prefix": "CICBIMS 2024",
        "toc_strategy": "dots",
        "toc_pages": (5, 9),
    },
    {
        "doc_id": "cic_beginner_cde",
        "path": HK_SOURCES_DIR / "CIC Beginner Guide-Adoption of CDE.pdf",
        "authority_prefix": "CIC CDE Beginner Guide",
        "toc_strategy": "outline",
    },
    {
        "doc_id": "devb_harmonisation_v3",
        "path": HK_SOURCES_DIR
        / "DEVB BIM Harmonisation Guidelines for WDs (v3_0) with All Appendices.pdf",
        "authority_prefix": "DEVB BIM Harmonisation v3.0",
        "toc_strategy": "devb_mixed",
        "main_body_end_page": 41,
    },
)

TEMPLATE_SOURCES = (
    {
        "doc_id": "template_d1",
        "path": HK_SOURCES_DIR
        / "CIC BIM Standards General 2024"
        / "D1_CIC BIM_OIR_Template.docx",
        "template_num": 1,
        "name": "OIR",
    },
    {
        "doc_id": "template_d2",
        "path": HK_SOURCES_DIR
        / "CIC BIM Standards General 2024"
        / "D2_CIC BIM_AIR_Template.docx",
        "template_num": 2,
        "name": "AIR",
    },
    {
        "doc_id": "template_d3",
        "path": HK_SOURCES_DIR
        / "CIC BIM Standards General 2024"
        / "D3_CIC BIM_PIR_Template.docx",
        "template_num": 3,
        "name": "PIR",
    },
    {
        "doc_id": "template_d4",
        "path": HK_SOURCES_DIR
        / "CIC BIM Standards General 2024"
        / "D4_CIC BIM_SIR_Template.docx",
        "template_num": 4,
        "name": "SIR",
    },
    {
        "doc_id": "template_d5",
        "path": HK_SOURCES_DIR
        / "CIC BIM Standards General 2024"
        / "D5_CIC Pre-Appointment Implementation Plan_Template.docx",
        "template_num": 5,
        "name": "Pre-Appointment IP",
    },
    {
        "doc_id": "template_d6",
        "path": HK_SOURCES_DIR
        / "CIC BIM Standards General 2024"
        / "D6_CIC Pre-Appointment BIM Execution Plan_Template.docx",
        "template_num": 6,
        "name": "Pre-Appointment BEP",
    },
    {
        "doc_id": "template_d7",
        "path": HK_SOURCES_DIR
        / "CIC BIM Standards General 2024"
        / "D7_CIC BIM Capability Assessment_Template.docx",
        "template_num": 7,
        "name": "Capability Assessment",
    },
    {
        "doc_id": "template_d8",
        "path": HK_SOURCES_DIR
        / "CIC BIM Standards General 2024"
        / "D8_CIC BIM Capability Summary Sheet and Schedule of Software Use.xlsx",
        "template_num": 8,
        "name": "Capability Summary",
    },
    {
        "doc_id": "template_d9",
        "path": HK_SOURCES_DIR
        / "CIC BIM Standards General 2024"
        / "D9_CIC Project Member Resume.docx",
        "template_num": 9,
        "name": "Project Member Resume",
    },
)


def section_url(doc_id: str, section_id: str) -> str:
    return f"hk_cde://{doc_id}/{section_id}"
