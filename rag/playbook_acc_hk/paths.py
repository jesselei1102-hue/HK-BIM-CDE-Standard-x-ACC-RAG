"""Playbook 路径常量。"""

from __future__ import annotations

from pathlib import Path

from rag.config import PROJECT_ROOT

PLAYBOOK_SOURCE_DIR = PROJECT_ROOT / "output" / "acc_hk_bim_playbook"
PLAYBOOK_KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge" / "playbook" / "acc_hk_bim"
PLAYBOOK_CORPUS_DIR = PLAYBOOK_KNOWLEDGE_DIR / "corpus"
PLAYBOOK_RESEARCH_DIR = PLAYBOOK_KNOWLEDGE_DIR / "research"
PLAYBOOK_QUERY_KB_PATH = PLAYBOOK_KNOWLEDGE_DIR / "query_kb.jsonl"
PLAYBOOK_SECTIONS_INDEX_PATH = PLAYBOOK_RESEARCH_DIR / "sections_index.jsonl"

PLAYBOOK_RAG_DATA_DIR = PROJECT_ROOT / ".rag_data" / "playbook_acc_hk"
PLAYBOOK_CHROMA_DIR = PLAYBOOK_RAG_DATA_DIR / "chroma"
PLAYBOOK_CHUNKS_PATH = PLAYBOOK_RAG_DATA_DIR / "chunks.jsonl"
PLAYBOOK_MANIFEST_PATH = PLAYBOOK_RAG_DATA_DIR / "manifest.json"
PLAYBOOK_KB_CHROMA_DIR = PLAYBOOK_RAG_DATA_DIR / "kb_chroma"
PLAYBOOK_KB_MANIFEST_PATH = PLAYBOOK_RAG_DATA_DIR / "kb_route_manifest.json"

PLAYBOOK_COLLECTION_NAME = "playbook_acc_hk"
PLAYBOOK_KB_COLLECTION_NAME = "playbook_acc_hk_route"


def playbook_url(chapter_id: str, section_slug: str | None = None) -> str:
    if section_slug:
        return f"playbook://acc_hk_bim/{chapter_id}/{section_slug}"
    return f"playbook://acc_hk_bim/{chapter_id}"
