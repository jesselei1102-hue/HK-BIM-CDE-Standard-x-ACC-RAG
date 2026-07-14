"""Playbook 段落硬钉：文件夹类 hybrid 必须用含目录树的 WIP 段。"""

from __future__ import annotations

import json
from pathlib import Path

from rag.orchestrator.merge import MergedContexts, TrackedChunk, merge_triple_contexts
from rag.retrieval import RetrievedChunk

WIP_FOLDER_URL_MARKER = "02_folder_cde/2_wip"
CONCEPT_URL_MARKER = "1_cde_四容器概念回顧"


def _chunk_from_record(record: dict) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=record["chunk_id"],
        title=record["title"],
        source_url=record["source_url"],
        source_file=record["source_file"],
        page_index=int(record["page_index"]),
        line_start=int(record["line_start"]),
        product=record["product"],
        chunk_index=int(record["chunk_index"]),
        chunk_count=int(record["chunk_count"]),
        token_count=int(record["token_count"]),
        text=record["text"],
        score=1.0,
        vector_similarity=0.99,
    )


def load_wip_folder_chunk(chunks_path: Path) -> RetrievedChunk | None:
    if not chunks_path.is_file():
        return None
    fallback: RetrievedChunk | None = None
    with chunks_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            url = record.get("source_url", "")
            if WIP_FOLDER_URL_MARKER not in url:
                continue
            chunk = _chunk_from_record(record)
            if "Central_Models" in chunk.text:
                return chunk
            fallback = chunk
    return fallback


def playbook_chunk_needs_folder_pin(chunk: RetrievedChunk) -> bool:
    url = chunk.source_url
    if CONCEPT_URL_MARKER in url:
        return True
    if WIP_FOLDER_URL_MARKER in url:
        return False
    # 概念段特征：无 01_WIP 树但有四容器表格
    return "01_WIP" not in chunk.text and "Work in Progress" in chunk.text


def pin_folder_playbook_in_merged(
    merged: MergedContexts,
    *,
    chunks_path: Path,
) -> tuple[MergedContexts, bool]:
    """若 Playbook 误召回概念段，替换为 WIP 目录树段并重新编号。"""
    playbook_items = [t for t in merged.tracked if t.track == "playbook"]
    if not playbook_items:
        return merged, False
    current = playbook_items[0].chunk
    if not playbook_chunk_needs_folder_pin(current):
        return merged, False

    replacement = load_wip_folder_chunk(chunks_path)
    if replacement is None:
        return merged, False

    docs = [t.chunk for t in merged.tracked if t.track == "docs"]
    industry = [t.chunk for t in merged.tracked if t.track == "hk_cde"]
    new_merged = merge_triple_contexts(
        docs_chunks=docs,
        industry_chunks=industry,
        playbook_chunks=[replacement],
        docs_top_k=len(docs) or 0,
        industry_top_k=len(industry) or 0,
        playbook_top_k=1,
    )
    return new_merged, True
