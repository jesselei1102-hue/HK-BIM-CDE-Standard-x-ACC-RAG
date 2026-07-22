"""Playbook 段落硬钉：文件夹类 hybrid 必须用含目录树的 WIP 段。"""

from __future__ import annotations

import json
from pathlib import Path

from rag.orchestrator.merge import MergedContexts, TrackedChunk, merge_triple_contexts
from rag.retrieval import RetrievedChunk

# New HK CDE Spec chapters (Buildings preferred, Civil fallback).
WIP_FOLDER_URL_MARKERS = (
    "11_buildings_folders_permissions",
    "21_civil_folders_permissions",
)
# Backward-compatible aliases for chunk_pin / tests
WIP_FOLDER_URL_MARKER = WIP_FOLDER_URL_MARKERS[0]
WIP_TREE_MARKERS = ("01_WIP", "Team_", "02_SHARED", "8_BIM")
CONCEPT_URL_MARKERS = (
    "00_hk_cde_spec_index",
    "overview_roles",
    "assets_midp_acceptance",
)
CONCEPT_URL_MARKER = CONCEPT_URL_MARKERS[0]


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


def _looks_like_folder_tree(text: str) -> bool:
    hits = sum(1 for marker in WIP_TREE_MARKERS if marker in text)
    return hits >= 2


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
            if not any(marker in url for marker in WIP_FOLDER_URL_MARKERS):
                continue
            chunk = _chunk_from_record(record)
            if _looks_like_folder_tree(chunk.text):
                # Prefer Buildings tree when both exist; first tree hit wins in file order
                # (11_buildings before 21_civil because chunks are written in ingest order).
                if "11_buildings_folders_permissions" in url:
                    return chunk
                fallback = chunk
            elif fallback is None:
                fallback = chunk
    return fallback


def playbook_chunk_needs_folder_pin(chunk: RetrievedChunk) -> bool:
    url = chunk.source_url
    if any(marker in url for marker in CONCEPT_URL_MARKERS):
        return True
    if any(marker in url for marker in WIP_FOLDER_URL_MARKERS):
        return not _looks_like_folder_tree(chunk.text)
    # 概念段特征：无 01_WIP 树
    return "01_WIP" not in chunk.text and (
        "Work in Progress" in chunk.text or "四容器" in chunk.text
    )


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
