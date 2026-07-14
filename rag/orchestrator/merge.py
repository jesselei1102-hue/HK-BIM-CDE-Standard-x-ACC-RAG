"""三轨检索结果分区合并与编号。"""

from __future__ import annotations

import os
from dataclasses import dataclass

from rag.retrieval import RetrievedChunk


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


@dataclass(frozen=True)
class TrackedChunk:
    chunk: RetrievedChunk
    track: str  # docs | hk_cde | playbook
    display_index: int


@dataclass(frozen=True)
class MergedContexts:
    docs_chunks: list[RetrievedChunk]
    industry_chunks: list[RetrievedChunk]
    playbook_chunks: list[RetrievedChunk]
    tracked: list[TrackedChunk]
    docs_indices: list[int]
    industry_indices: list[int]
    playbook_indices: list[int]


def merge_dual_contexts(
    docs_chunks: list[RetrievedChunk],
    industry_chunks: list[RetrievedChunk],
    *,
    docs_top_k: int | None = None,
    industry_top_k: int | None = None,
    maximum_context_tokens: int | None = None,
    playbook_chunks: list[RetrievedChunk] | None = None,
    playbook_top_k: int | None = None,
) -> MergedContexts:
    """合并 HK + Playbook + Docs；playbook 可选。"""
    return merge_triple_contexts(
        docs_chunks=docs_chunks,
        industry_chunks=industry_chunks,
        playbook_chunks=playbook_chunks or [],
        docs_top_k=docs_top_k,
        industry_top_k=industry_top_k,
        playbook_top_k=playbook_top_k,
        maximum_context_tokens=maximum_context_tokens,
    )


def merge_triple_contexts(
    *,
    docs_chunks: list[RetrievedChunk],
    industry_chunks: list[RetrievedChunk],
    playbook_chunks: list[RetrievedChunk],
    docs_top_k: int | None = None,
    industry_top_k: int | None = None,
    playbook_top_k: int | None = None,
    maximum_context_tokens: int | None = None,
) -> MergedContexts:
    docs_limit = docs_top_k if docs_top_k is not None else _env_int(
        "HYBRID_DOCS_TOP_K", 2
    )
    industry_limit = industry_top_k if industry_top_k is not None else _env_int(
        "HYBRID_INDUSTRY_TOP_K", 1
    )
    playbook_limit = playbook_top_k if playbook_top_k is not None else _env_int(
        "HYBRID_PLAYBOOK_TOP_K", 1
    )
    max_tokens = maximum_context_tokens if maximum_context_tokens is not None else _env_int(
        "RAG_MAX_CONTEXT_TOKENS", 2_000
    )

    selected_docs = docs_chunks[:docs_limit]
    selected_industry = industry_chunks[:industry_limit]
    selected_playbook = playbook_chunks[:playbook_limit]

    tracked: list[TrackedChunk] = []
    docs_indices: list[int] = []
    industry_indices: list[int] = []
    playbook_indices: list[int] = []
    used_tokens = 0
    display = 1

    def _try_add(chunk: RetrievedChunk, track: str) -> bool:
        nonlocal used_tokens, display
        if tracked and used_tokens + chunk.token_count > max_tokens:
            return False
        tracked.append(TrackedChunk(chunk=chunk, track=track, display_index=display))
        if track == "hk_cde":
            industry_indices.append(display)
        elif track == "playbook":
            playbook_indices.append(display)
        else:
            docs_indices.append(display)
        used_tokens += chunk.token_count
        display += 1
        return True

    # 先各轨保底 1 条，避免 token 预算把 Docs 挤掉
    queues = [
        ("hk_cde", list(selected_industry)),
        ("playbook", list(selected_playbook)),
        ("docs", list(selected_docs)),
    ]
    for track, queue in queues:
        if queue:
            _try_add(queue.pop(0), track)

    # 再按 标准 → 实施 → 产品 补齐剩余
    for track, queue in queues:
        while queue:
            if not _try_add(queue.pop(0), track):
                break

    return MergedContexts(
        docs_chunks=[item.chunk for item in tracked if item.track == "docs"],
        industry_chunks=[item.chunk for item in tracked if item.track == "hk_cde"],
        playbook_chunks=[item.chunk for item in tracked if item.track == "playbook"],
        tracked=tracked,
        docs_indices=docs_indices,
        industry_indices=industry_indices,
        playbook_indices=playbook_indices,
    )


def format_partitioned_context(merged: MergedContexts) -> str:
    hk_blocks: list[str] = []
    playbook_blocks: list[str] = []
    docs_blocks: list[str] = []
    for item in merged.tracked:
        body = item.chunk.text
        if len(body) > 1800:
            body = body[:1800] + "\n..."
        block = (
            f"[{item.display_index}] {item.chunk.title}\n"
            f"Source: {item.chunk.source_url}\n"
            f"{body}"
        )
        if item.track == "hk_cde":
            hk_blocks.append(block)
        elif item.track == "playbook":
            playbook_blocks.append(block)
        else:
            docs_blocks.append(block)

    parts: list[str] = []
    if hk_blocks:
        parts.append("## HK CDE 资料\n\n" + "\n\n".join(hk_blocks))
    if playbook_blocks:
        parts.append("## 实施手册资料\n\n" + "\n\n".join(playbook_blocks))
    if docs_blocks:
        parts.append("## Docs 资料\n\n" + "\n\n".join(docs_blocks))
    return "\n\n".join(parts) if parts else "(无资料)"


def format_hybrid_sources(merged: MergedContexts) -> list[str]:
    lines: list[str] = []
    label_map = {
        "hk_cde": "[HK CDE]",
        "playbook": "[Playbook]",
        "docs": "[Docs]",
    }
    for item in merged.tracked:
        label = label_map.get(item.track, f"[{item.track}]")
        lines.append(
            f"[{item.display_index}] {label} {item.chunk.title}\n"
            f"    {item.chunk.source_url}"
        )
    return lines
